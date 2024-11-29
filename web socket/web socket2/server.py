# server.py
import asyncio
import websockets

async def echo(websocket, path):
    async for message in websocket:
        print(f"Received message from client: {message}")
        await websocket.send(f"Echo: {message}")  # Send the message back to the client

# Run the server on localhost:8765
start_server = websockets.serve(echo, "localhost", 8765)

# Start the server asynchronously
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
