import cv2
import asyncio
import websockets
import base64

async def send_video(channel):
    uri = f"ws://localhost:5678/{channel}"
    cap = cv2.VideoCapture(0)  # Or whatever your video source is
    async with websockets.connect(uri) as websocket:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            _, buffer = cv2.imencode('.jpg', frame)
            await websocket.send(base64.b64encode(buffer).decode())

# Replace "channel1" with the desired channel name
asyncio.get_event_loop().run_until_complete(send_video("channel1"))
