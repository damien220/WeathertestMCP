- **MCP Server**: Handles structured requests.
- **JSON Schema Validation**: Ensures requests are valid.
- **Client**: Sends MCP requests.
- **Tool Logic**: Example tool `get_weather`.

Install Required Packages
pip install websockets jsonschema

Run the Example

1. Start the server:
    python mcp_server.py
    
2. Run the client in another terminal:
    python mcp_client.py
    
Output:
Server response: {"type": "response", "id": "req_001", "status": "success", "result": {"location": "Berlin", "temperature": 22, "units": "metric", "condition": "Sunny"}}
