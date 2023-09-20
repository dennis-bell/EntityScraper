import asyncio
from database import initialize_db
from ha_connection import connect_to_ha

# Main execution
async def main():
    # Initialize DB
    initialize_db()
    
    # Start the connection to HA
    await connect_to_ha()

# Running the main loop
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
