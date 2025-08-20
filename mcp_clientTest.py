import asyncio
import websockets
import json

async def test_mcp_server():
    uri = "ws://localhost:8000/mcp"
    
    try:
        async with websockets.connect(uri) as websocket:
            print("✓ Connected to MCP server")
            
            # Test 1: Initialize
            init_msg = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"resources": {}, "tools": {}},
                    "clientInfo": {"name": "test-client", "version": "1.0"}
                }
            }
            
            await websocket.send(json.dumps(init_msg))
            response = await websocket.recv()
            print(f"✓ Initialize response: {json.loads(response)['result']['serverInfo']['name']}")
            
            # Test 2: List tools
            tools_msg = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/list"
            }
            
            await websocket.send(json.dumps(tools_msg))
            response = await websocket.recv()
            tools = json.loads(response)['result']['tools']
            print(f"✓ Found {len(tools)} tools: {[t['name'] for t in tools]}")
            
            # Test 3: Call echo tool
            echo_msg = {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {
                    "name": "echo",
                    "arguments": {"message": "Hello from test client!"}
                }
            }
            
            await websocket.send(json.dumps(echo_msg))
            response = await websocket.recv()
            result = json.loads(response)['result']['content'][0]['text']
            print(f"✓ Echo response: {result}")
            
            print("\\n MCP server is fully functional!")
            
    except Exception as e:
        print(f" Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_mcp_server())
