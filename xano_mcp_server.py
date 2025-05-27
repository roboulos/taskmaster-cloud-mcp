# Simplified Xano MCP Server using standard HTTP server
import argparse
import json
import asyncio
import httpx
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

class XanoMCPHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, xano_token=None, **kwargs):
        self.xano_token = xano_token
        self.http_client = httpx.Client(
            headers={
                "Authorization": f"Bearer {xano_token}",
                "Content-Type": "application/json"
            },
            timeout=30.0
        )
        super().__init__(*args, **kwargs)

    def _set_headers(self, content_type="application/json"):
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def do_GET(self):
        # Handle GET requests (like listing available tools)
        if self.path == "/tools":
            self._set_headers()
            tools = self._get_available_tools()
            self.wfile.write(json.dumps(tools).encode())
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        # Handle POST requests (tool execution)
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        request_data = json.loads(post_data.decode('utf-8'))
        
        # Parse the tool name from the path
        tool_name = self.path.strip("/").split("/")[-1]
        
        if tool_name == "xano_list_instances":
            result = self._list_instances()
            self._set_headers()
            self.wfile.write(json.dumps(result).encode())
        elif tool_name == "xano_get_instance":
            name = request_data.get("name", "")
            result = self._get_instance(name)
            self._set_headers()
            self.wfile.write(json.dumps(result).encode())
        else:
            self.send_error(404, f"Tool {tool_name} not found")

    def _get_available_tools(self):
        # Return list of available tools
        return [
            {
                "name": "xano_list_instances",
                "description": "Lists all Xano instances available to the authenticated user"
            },
            {
                "name": "xano_get_instance",
                "description": "Gets details about a specific Xano instance"
            }
            # Add more tools here...
        ]

    def _list_instances(self):
        try:
            response = self.http_client.get("https://app.xano.com/api/meta/instance")
            response.raise_for_status()
            return {"instances": response.json()}
        except Exception as e:
            return {"error": f"Failed to list Xano instances: {str(e)}"}

    def _get_instance(self, name):
        try:
            response = self.http_client.get(f"https://app.xano.com/api/meta/instance/{name}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": f"Failed to get Xano instance {name}: {str(e)}"}

def run_server(token, port=3000):
    # Create a custom handler class with the token
    handler = lambda *args, **kwargs: XanoMCPHandler(*args, xano_token=token, **kwargs)
    
    # Start the server
    server = HTTPServer(('localhost', port), handler)
    print(f"Starting Xano MCP server on port {port}")
    server.serve_forever()

def main():
    parser = argparse.ArgumentParser(description="MCP Server for Xano integration")
    parser.add_argument("--token", required=True, help="Xano Metadata API access token")
    parser.add_argument("--port", type=int, default=3000, help="Port to run the server on")
    args = parser.parse_args()
    
    run_server(args.token, args.port)

if __name__ == "__main__":
    main()