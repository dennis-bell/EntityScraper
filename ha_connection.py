import asyncio
import websockets
import json
from .database import update_entity_state
from .config import HA_WS_URL, RETRY_MAX, BASE_RETRY_DELAY

async def connect_to_ha():
    retries = 0
    delay = BASE_RETRY_DELAY

    while retries < RETRY_MAX:
        try:
            async with websockets.connect(HA_WS_URL) as ws:
                # Authentication message (fill in with your actual token)
                auth_msg = {
                    'type': 'auth',
                    'access_token': 'YOUR_LONG_LIVED_ACCESS_TOKEN'
                }
                await ws.send(json.dumps(auth_msg))
                auth_resp = await ws.recv()
                if json.loads(auth_resp)["type"] == "auth_ok":
                    await ws.send(json.dumps({'id': 1, 'type': 'subscribe_events', 'event_type': 'state_changed'}))
                    while True:
                        message = await ws.recv()
                        message_data = json.loads(message)
                        if message_data["type"] == "event":
                            entity_id = message_data["event"]["data"]["entity_id"]
                            state = message_data["event"]["data"]["new_state"]["state"]
                            if state == 'unavailable':
                                await update_entity_state(entity_id, state)
                else:
                    print("Authentication failed!")
                    break

                # If we are here, the connection is successful. Reset retries.
                retries = 0
                delay = BASE_RETRY_DELAY

        except websockets.ConnectionClosed:
            print(f"WebSocket connection closed. Retrying in {delay} seconds...")
            retries += 1
            await asyncio.sleep(delay)
            delay *= 2  # Double the delay for exponential backoff

        except Exception as e:
            print(f"Error encountered: {e}. Retrying in {delay} seconds...")
            retries += 1
            await asyncio.sleep(delay)
            delay *= 2  # Double the delay for exponential backoff


# Health check for WebSocket
async def health_check(ws):
    while True:
        if not ws.open:
            print("WebSocket connection lost. Attempting to reconnect...")
            await connect_to_ha()
        await asyncio.sleep(30)  # Check every 30 seconds