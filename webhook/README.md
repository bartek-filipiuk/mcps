# Webhook MCP Server

A simple Model Context Protocol (MCP) server that provides a single tool for sending webhook requests. This server integrates with Windsurf IDE through the MCP protocol, allowing AI assistants to trigger webhook calls.

## How It Works

The Webhook MCP Server is built using Python with the MCP SDK. It operates as follows:

1. The server initializes with the FastMCP framework, identifying itself as "webhook-mcp-server"
2. It reads configuration from the MCP config file located at `/home/bartek/.codeium/windsurf/mcp_config.json`
3. When the `send_webhook` tool is called, it:
   - Retrieves the webhook URL from the configuration
   - Converts the provided payload to JSON
   - Sends a POST request to the webhook URL with the appropriate headers
   - Returns the response details to the caller

The server uses stdio transport for communication with Windsurf, making it compatible with the Windsurf IDE's MCP client.

## Available Functions

The server provides a single tool:

### `send_webhook`

**Description**: Sends a POST request to the configured webhook URL with the provided payload.

**Parameters**:
- `payload` (Dict[str, Any]): A dictionary containing the data to send. This will be converted to JSON.

**Returns**: A dictionary with:
- `status_code`: HTTP status code of the response
- `headers`: Response headers as a dictionary
- `content`: Response body content as text
- `error`: Error message (if an error occurred)

## Payload Structure

The payload can be any valid JSON-serializable dictionary. There are no specific requirements for the structure, as long as it can be converted to valid JSON. Here are some examples:

### Simple Payload
```json
{
  "message": "Hello from Webhook MCP!",
  "timestamp": "2025-03-29T11:28:53+01:00"
}
```

### Complex Payload
```json
{
  "message": "Hello from Webhook MCP!",
  "timestamp": "2025-03-29T11:28:53+01:00",
  "test": true,
  "data": {
    "key1": "value1",
    "key2": 42,
    "nested": {
      "array": [1, 2, 3],
      "object": {"a": "b"}
    }
  },
  "array_example": ["item1", "item2", "item3"]
}
```

The webhook endpoint is responsible for parsing and processing the JSON payload according to its own requirements.

## Setup

### Local Development Setup

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Update your MCP configuration file at `/home/bartek/.codeium/windsurf/mcp_config.json` to include the webhook server:

```json
{
  "mcpServers": {
    "webhook-mcp-server": {
      "command": "python3",
      "args": [
        "/home/bartek/www/mcps/webhook/webhook_server.py"
      ],
      "env": {
        "WEBHOOK_URL": "https://your-webhook-url.com/endpoint"
      }
    }
  }
}
```

3. Replace `"https://your-webhook-url.com/endpoint"` with your actual webhook URL.

## Usage in Windsurf

When using this MCP server with Windsurf IDE, the AI assistant will be able to send webhook requests to your configured webhook URL. The webhook functionality will be available to the AI assistant automatically after configuration.

### Windsurf/Cursor Configuration

For Windsurf or Cursor IDE, add the following configuration to your MCP config file (typically located at `~/.codeium/windsurf/mcp_config.json`):

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

Make sure to replace the webhook URL with your own endpoint if needed.

## Integration with AI Assistant Applications

### Adding to Cherry Studio

To add this webhook MCP server to Cherry Studio or similar AI assistant applications:

1. Open the AI assistant application settings
2. Navigate to the MCP Server configuration section
3. Add a new MCP Server with the following details:

   - **Name**: `webhook-mcp-server`
   - **Description**: `Webhook MCP Server for sending webhook requests`
   - **Type**: `STDIO` (Standard Input/Output)
   - **Command**: `python3`
   - **Arguments**: `/path/to/webhook_server.py` (Full path to the webhook_server.py script)
   - **Environment Variables**:
     ```
     WEBHOOK_URL=https://your-webhook-url.com/endpoint
     CONFIG_PATH=/path/to/your/config.json
     ```

4. Save the configuration
5. The webhook tool will now be available to the AI assistant as `send_webhook`

> **Important**: The default implementation looks for the config file at `/home/bartek/.codeium/windsurf/mcp_config.json`. When using with Cherry Studio or other applications, you should either:
> 
> 1. Modify the `config_path` in `webhook_server.py` to point to your application's config file
> 2. Set the `CONFIG_PATH` environment variable when configuring the MCP server
> 3. Create a symbolic link from your application's config to the expected path
> 4. Use the HTTP server version which can read the webhook URL directly from environment variables


## Troubleshooting

- **Config File Not Found**: Ensure the config file path is correct for your environment
- **Webhook URL Not Configured**: Check that the WEBHOOK_URL is properly set in your config or environment variables
- **Connection Errors**: Verify that the webhook URL is accessible from your server
- **Permission Issues**: Ensure the service has proper permissions to read the config file and execute the script
