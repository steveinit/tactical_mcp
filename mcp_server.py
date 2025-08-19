import socket, json
s = socket.socket()
s.connect(('httpbin.org', 80))
mcp = json.dumps({'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2024-11-05'}})
s.send(f'POST /post HTTP/1.1\r\nHost: httpbin.org\r\nContent-Type: application/json\r\nContent-Length: {len(mcp)}\r\n\r\n{mcp}'.encode())
print('MCP traffic sent')
s.close()
