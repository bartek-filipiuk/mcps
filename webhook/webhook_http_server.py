#!/usr/bin/env python3
"""
HTTP Server version of the webhook MCP server
This version exposes the webhook functionality via HTTP endpoints
"""
from typing import Any, Dict
import os
import json
import httpx
import uvicorn
from fastapi import FastAPI, HTTPException, Request

# Create FastAPI app
app = FastAPI(title="Webhook HTTP Server")

def read_config():
    """Read the MCP config file to get environment variables"""
    # Allow config path to be specified via environment variable
    config_path = os.environ.get("CONFIG_PATH", "/home/bartek/.codeium/windsurf/mcp_config.json")
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

@app.get("/")
async def root():
    """Root endpoint with basic info"""
    return {
        "name": "Webhook HTTP Server",
        "description": "HTTP server version of the webhook MCP server",
        "endpoints": [
            {"path": "/", "method": "GET", "description": "This information"},
            {"path": "/webhook", "method": "POST", "description": "Send a webhook request"}
        ]
    }

@app.post("/webhook")
async def webhook(request: Request):
    """Send a webhook request with the provided payload"""
    try:
        # Parse the JSON payload from the request
        payload = await request.json()
        
        # Get environment variables from config
        env_vars = read_config()
        webhook_url = env_vars.get("WEBHOOK_URL")
        
        if not webhook_url:
            raise HTTPException(status_code=500, detail="WEBHOOK_URL not configured in environment variables")
        
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
        raise HTTPException(status_code=500, detail=f"Error sending webhook: {str(e)}")

if __name__ == "__main__":
    # Run the server on localhost:8000
    print("Starting Webhook HTTP Server on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
