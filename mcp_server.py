# mcp_server.py
import asyncio
import json
import websockets
from jsonschema import validate, ValidationError

# --- JSON Schema for MCP requests ---
mcp_request_schema = {
    "type": "object",
    "properties": {
        "type": {"type": "string", "enum": ["request"]},
        "id": {"type": "string"},
        "tool": {"type": "string"},
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string"},
                "units": {"type": "string", "enum": ["metric", "imperial"]}
            },
            "required": ["location"]
        }
    },
    "required": ["type", "id", "tool", "parameters"]
}

# --- Example tool implementation ---
def get_weather(location, units="metric"):
    # Normally you'd call a real API, but we'll simulate.
    return {
        "location": location,
        "temperature": 22 if units == "metric" else 71,
        "units": units,
        "condition": "Sunny"
    }

# --- Handle incoming requests ---
async def handle_message(message):
    try:
        validate(instance=message, schema=mcp_request_schema)
    except ValidationError as e:
        return {
            "type": "error",
            "id": message.get("id", "unknown"),
            "error": f"Schema validation failed: {e.message}"
        }

    tool = message["tool"]
    params = message["parameters"]

    if tool == "get_weather":
        result = get_weather(params["location"], params.get("units", "metric"))
        return {"type": "response", "id": message["id"], "status": "success", "result": result}
    else:
        return {"type": "error", "id": message["id"], "error": f"Unknown tool: {tool}"}

# --- WebSocket server logic ---
async def mcp_server(websocket):
    async for raw_msg in websocket:
        try:
            message = json.loads(raw_msg)
            response = await handle_message(message)
        except json.JSONDecodeError:
            response = {"type": "error", "id": "unknown", "error": "Invalid JSON format"}
        await websocket.send(json.dumps(response))

async def main():
    async with websockets.serve(mcp_server, "localhost", 8765):
        print("✅ MCP Server running on ws://localhost:8765")
        await asyncio.Future()  # keep running

if __name__ == "__main__":
    asyncio.run(main())
