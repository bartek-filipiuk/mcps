# Webhook MCP Server - Quick Setup Guide

This guide provides concise instructions for setting up the webhook MCP server in IDEs like Windsurf or Cherry Studio.

## Prerequisites

- Python 3.7+
- Required packages: `mcp`, `httpx`
- A webhook URL to send requests to

## Installation

```bash
pip install -r requirements.txt
```

## Setup in Windsurf/Cursor

1. Open Windsurf or Cursor IDE
2. Navigate to Settings > MCP Servers
3. Add a new MCP Server with these details:
   - **Name**: `webhook-mcp-server`
   - **Type**: `STDIO`
   - **Command**: `python3`
   - **Arguments**: `/home/bartek/www/mcps/webhook/webhook_server.py`
   - **Environment Variables**:
     ```
     WEBHOOK_URL=https://hook.eu2.make.com/xrjy1agher38t9bj1o2vfrv43s41g3rd
     ```

4. Save the configuration
5. The webhook tool will be available as `mcp2_send_webhook`

Alternatively, you can directly edit your MCP config file (typically located at `~/.codeium/windsurf/mcp_config.json`) and add the following configuration:

```json
{
  "mcpServers": {
    "webhook-mcp-server": {
      "command": "python3",
      "args": [
        "/home/bartek/www/mcps/webhook/webhook_server.py"
      ],
      "env": {
        "WEBHOOK_URL": "https://hook.eu2.make.com/xrjy1agher38t9bj1o2vfrv43s41g3rd"
      }
    }
  }
}
```

This is a real-world example from a working configuration. You should replace the webhook URL with your own endpoint URL if needed.

## Setup in Cherry Studio

1. Open Cherry Studio
2. Go to Settings > Integrations > MCP Servers
3. Add a new MCP Server with these details:
   - **Name**: `webhook-mcp-server`
   - **Description**: `Webhook MCP Server for sending webhook requests`
   - **Type**: `STDIO`
   - **Command**: `python3`
   - **Arguments**: `/path/to/webhook_server.py`
   - **Environment Variables**:
     ```
     WEBHOOK_URL=https://your-webhook-url.com/endpoint
     CONFIG_PATH=/path/to/your/config.json
     ```

4. Save the configuration
5. The webhook tool will be available as `send_webhook`

## Important Configuration Notes

- The default implementation looks for config at `/home/bartek/.codeium/windsurf/mcp_config.json`
- When using with Cherry Studio or other applications, either:
  - Set the `CONFIG_PATH` environment variable as shown above
  - Modify the `config_path` in `webhook_server.py`
  - Create a symbolic link from your application's config to the expected path

## Example Configuration JSON

Here's an example of how the webhook MCP server should be configured in your MCP configuration file:

```json
{
  "mcpServers": {
    "webhook-mcp-server": {
      "command": "python3",
      "args": [
        "/home/bartek/www/mcps/webhook/webhook_server.py"
      ],
      "env": {
        "WEBHOOK_URL": "https://hook.eu2.make.com/xrjy1agher38t9bj1o2vfrv43s41g3rd"
      }
    }
  }
}
```

This is a real-world example from a working configuration. You should replace the webhook URL with your own endpoint URL.

## Using the Webhook

Once configured, the webhook functionality will be available to the AI assistant in your IDE. The webhook will send data to the URL you specified in the configuration.

### Payload Structure Example

When using the webhook, you can send JSON payloads with structures like:

```json
{
  "message": "Hello from AI Assistant!",
  "timestamp": "2025-03-29T21:46:50+01:00",
  "data": {
    "key1": "value1",
    "key2": 42
  }
}
```

## Alternative: HTTP Server Version

For applications without MCP support, use the HTTP server version:

1. Start the server:
   ```bash
   python3 webhook_http_server.py
   ```

2. Send requests to `http://localhost:8000/webhook` using any HTTP client
