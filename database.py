import sqlite3

DB_PATH = 'entity_states.db'

def update_entity_state(entity_id, state):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS entity_states
                         (entity_id text, state text, last_updated timestamp)''')
        cursor.execute("INSERT OR REPLACE INTO entity_states VALUES (?, ?, datetime('now'))", (entity_id, state))
        conn.commit()

def initialize_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS entity_states
                         (entity_id text, state text, last_updated timestamp)''')
        conn.commit()
