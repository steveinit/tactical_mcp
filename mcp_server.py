from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn
import json
import asyncio

app = FastAPI(title="[test_name] MCP Server")

@app.get("/")
async def root():
    return {
        "message": "Beethoven MCP Server Running",
        "websocket_endpoint": "ws://[your-ip]:8000/mcp"
    }

@app.websocket("/mcp")
async def mcp_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("MCP client connected!")
    
    try:
        while True:
            # Receive MCP message
            message = await websocket.receive_text()
            data = json.loads(message)
            print(f"Received: {data.get('method', 'unknown')}")
            
            # Handle MCP methods
            if data.get("method") == "initialize":
                response = {
                    "jsonrpc": "2.0",
                    "id": data.get("id"),
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "serverInfo": {
                            "name": "test-mcp",
                            "version": "1.0.0"
                        },
                        "capabilities": {
                            "resources": {},
                            "tools": {}
                        }
                    }
                }
                
            elif data.get("method") == "tools/list":
                response = {
                    "jsonrpc": "2.0",
                    "id": data.get("id"),
                    "result": {
                        "tools": [
                            {
                                "name": "echo",
                                "description": "Echo back your message",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "message": {"type": "string"}
                                    }
                                }
                            }
                        ]
                    }
                }
                
            elif data.get("method") == "tools/call":
                tool_name = data.get("params", {}).get("name")
                arguments = data.get("params", {}).get("arguments", {})
                
                if tool_name == "echo":
                    message = arguments.get("message", "Hello from [test_name]!")
                    response = {
                        "jsonrpc": "2.0",
                        "id": data.get("id"),
                        "result": {
                            "content": [{
                                "type": "text",
                                "text": f"Echo: {message}"
                            }]
                        }
                    }
                else:
                    response = {
                        "jsonrpc": "2.0",
                        "id": data.get("id"),
                        "error": {
                            "code": -32601,
                            "message": f"Unknown tool: {tool_name}"
                        }
                    }
            else:
                response = {
                    "jsonrpc": "2.0",
                    "id": data.get("id"),
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {data.get('method')}"
                    }
                }
            
            # Send response
            await websocket.send_text(json.dumps(response))
            print(f"Sent response for: {data.get('method')}")
            
    except WebSocketDisconnect:
        print("MCP client disconnected")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Starting MCP Server...")
    print("HTTP: http://localhost:8000")
    print("WebSocket: ws://localhost:8000/mcp")
    uvicorn.run(app, host="0.0.0.0", port=8000)
