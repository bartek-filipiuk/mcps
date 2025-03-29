#!/usr/bin/env python3
"""
MCP Server with a single webhook tool
"""
from typing import Any, Dict
import os
import json
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server with proper name
mcp = FastMCP("webhook-mcp-server")

def read_config():
    """Read the MCP config file to get environment variables"""
    config_path = "/home/bartek/.codeium/windsurf/mcp_config.json"
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
            # Extract environment variables from config
            if 'mcpServers' in config:
                for server_name, server_config in config['mcpServers'].items():
                    if server_name == "webhook-mcp-server" and 'env' in server_config:
                        return server_config['env']
            return {}
    except Exception as e:
        print(f"Error reading config file: {str(e)}")
        return {}

@mcp.tool()
async def send_webhook(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Send a POST request to the configured webhook URL.
    
    Args:
        payload: Dictionary containing the data to send (will be converted to JSON)
    """
    # Get environment variables from config
    env_vars = read_config()
    webhook_url = env_vars.get("WEBHOOK_URL")
    
    if not webhook_url:
        return {"error": "WEBHOOK_URL not configured in environment variables"}
    
    try:
        # Ensure payload is properly formatted as JSON
        json_payload = json.dumps(payload)
        
        # Set headers for JSON content
        headers = {"Content-Type": "application/json"}
        
        # Send POST request to webhook URL
        async with httpx.AsyncClient() as client:
            response = await client.post(
                webhook_url, 
                headers=headers, 
                content=json_payload
            )
            
            return {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "content": response.text
            }
    except Exception as e:
        return {"error": f"Error sending webhook: {str(e)}"}

if __name__ == "__main__":
    # Initialize and run the server with stdio transport
    mcp.run(transport='stdio')
