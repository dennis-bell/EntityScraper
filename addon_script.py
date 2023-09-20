from flask import Flask, jsonify
import aiohttp
import asyncio
import sqlite3

app = Flask(__name__)

HASS_URL = 'http://your_homeassistant_ip:8123'
TOKEN = 'YOUR_LONG_LIVED_ACCESS_TOKEN'
HEADERS = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json'
}

DATABASE_PATH = '/data/unavailable_entities.db'  # '/data' is the mounted volume path

def db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    return conn

async def update_unavailable_entities():
    conn = db_connection()
    cursor = conn.cursor()
    
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{HASS_URL}/api/states', headers=HEADERS) as resp:
            states = await resp.json()

    for entity in states:
        if entity['state'] == 'unavailable':
            cursor.execute("INSERT OR IGNORE INTO unavailable_entities (entity_id, timestamp) VALUES (?, ?)", (entity['entity_id'], entity['last_changed']))
        else:
            cursor.execute("DELETE FROM unavailable_entities WHERE entity_id=?", (entity['entity_id'],))
    
    conn.commit()
    cursor.close()
    conn.close()

@app.route('/unavailable_entities', methods=['GET'])
def get_unavailable_entities():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM unavailable_entities")
    entities = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(entities)

if __name__ == '__main__':
    # Initialize database if it doesn't exist yet
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS unavailable_entities (
                       entity_id TEXT PRIMARY KEY,
                       timestamp TEXT NOT NULL)''')
    conn.commit()
    cursor.close()
    conn.close()

    loop = asyncio.get_event_loop()
    loop.create_task(update_unavailable_entities())
    app.run(host='0.0.0.0', port=5000)
