#!/usr/bin/env python3
"""
Test script for the Xano MCP Server.
This script tests the connection to both Xano and the MCP server.
"""

import argparse
import json
import httpx
import asyncio
import sys

async def test_xano_connection(token):
    """Test the connection to Xano's Metadata API"""
    print("Testing connection to Xano's Metadata API...")
    
    async with httpx.AsyncClient(
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        timeout=30.0
    ) as client:
        try:
            response = await client.get("https://app.xano.com/api/meta/instance")
            response.raise_for_status()
            instances = response.json()
            
            print("✅ Successfully connected to Xano's Metadata API")
            print(f"Found {len(instances)} instances:")
            
            for instance in instances:
                print(f"  - {instance.get('name', 'Unknown')}: {instance.get('display', 'No display name')}")
            
            return True
        except Exception as e:
            print(f"❌ Failed to connect to Xano's Metadata API: {str(e)}")
            return False

async def test_mcp_server(host, port, tool_name="xano_list_instances", params=None):
    """Test the connection to the MCP server"""
    print(f"\nTesting connection to MCP server at {host}:{port}...")
    
    mcp_url = f"http://{host}:{port}/tools"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            # First, check if the server is running by listing available tools
            response = await client.get(mcp_url)
            response.raise_for_status()
            tools = response.json()
            
            print("✅ Successfully connected to MCP server")
            print(f"Available tools:")
            
            for tool in tools:
                print(f"  - {tool.get('name')}: {tool.get('description', 'No description')}")
            
            # Now test a specific tool
            print(f"\nTesting tool: {tool_name}")
            params = params or {}
            
            response = await client.post(
                f"{mcp_url}/{tool_name}",
                json=params
            )
            
            response.raise_for_status()
            result = response.json()
            
            print(f"✅ Successfully called tool: {tool_name}")
            print("Result:")
            print(json.dumps(result, indent=2))
            
            return True
        except Exception as e:
            print(f"❌ Failed to test MCP server: {str(e)}")
            return False

async def main():
    parser = argparse.ArgumentParser(description="Test the Xano MCP Server")
    parser.add_argument("--token", required=True, help="Xano Metadata API access token")
    parser.add_argument("--host", default="localhost", help="MCP server host")
    parser.add_argument("--port", type=int, default=3000, help="MCP server port")
    args = parser.parse_args()
    
    # Test Xano connection
    xano_success = await test_xano_connection(args.token)
    
    # Test MCP server connection
    mcp_success = await test_mcp_server(args.host, args.port)
    
    # Summary
    print("\n--- Test Summary ---")
    print(f"Xano API Connection: {'✅ Passed' if xano_success else '❌ Failed'}")
    print(f"MCP Server Connection: {'✅ Passed' if mcp_success else '❌ Failed'}")
    
    if xano_success and mcp_success:
        print("\n🎉 All tests passed! Your Xano MCP Server is ready to use with Claude.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
