import asyncio
import websockets

channels = {}  # Maps channel names to sets of websockets subscribed to them

async def register(websocket, channel):
    if channel not in channels:
        channels[channel] = set()
    channels[channel].add(websocket)

async def unregister(websocket, channel):
    if channel in channels:
        channels[channel].remove(websocket)
        if not channels[channel]:  # Remove channel if it's empty
            del channels[channel]

async def relay_video(websocket, path):
    channel = path.strip("/")  # Use URL path as channel identifier
    await register(websocket, channel)
    try:
        async for message in websocket:
            # Relay message to all clients in the same channel
            if channel in channels:
                websockets_to_send = channels[channel].copy()
                if websocket in websockets_to_send:
                    websockets_to_send.remove(websocket)  # Optionally, don't echo messages to the sender
                for client in websockets_to_send:
                    await client.send(message)
    finally:
        await unregister(websocket, channel)

start_server = websockets.serve(relay_video, "0.0.0.0", 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
