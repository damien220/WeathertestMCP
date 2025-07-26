# mcp_client.py
import asyncio
import json
import websockets

async def send_mcp_request():
    async with websockets.connect("ws://localhost:8765") as websocket:
        # Send a valid request
        request = {
            "type": "request",
            "id": "req_001",
            "tool": "get_weather",
            "parameters": {"location": "Berlin", "units": "metric"}
        }

        await websocket.send(json.dumps(request))
        response = await websocket.recv()
        print("Server response:", response)

asyncio.run(send_mcp_request())
