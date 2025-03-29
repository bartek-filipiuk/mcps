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

### Server Deployment

When deploying to a server environment, you'll need to modify the following:

1. **Config File Path**: In `webhook_server.py`, modify the `config_path` variable in the `read_config()` function to point to your server's configuration file location:

```python
config_path = "/path/to/your/server/config.json"
```

2. **Configuration Options**: Create a configuration file on your server with the following structure:

```json
{
  "mcpServers": {
    "webhook-mcp-server": {
      "env": {
        "WEBHOOK_URL": "https://your-webhook-url.com/endpoint"
      }
    }
  }
}
```

3. **Alternative Environment Variables**: As an alternative to using the config file, you can modify the code to read from environment variables directly:

```python
webhook_url = os.environ.get("WEBHOOK_URL") or env_vars.get("WEBHOOK_URL")
```

4. **Running as a Service**: To run the webhook MCP server as a service on your server:

   a. Create a systemd service file (for Linux servers):
   ```
   [Unit]
   Description=Webhook MCP Server
   After=network.target

   [Service]
   User=your_user
   WorkingDirectory=/path/to/webhook/directory
   ExecStart=/usr/bin/python3 /path/to/webhook_server.py
   Restart=always
   Environment=WEBHOOK_URL=https://your-webhook-url.com/endpoint

   [Install]
   WantedBy=multi-user.target
   ```

   b. Install and start the service:
   ```bash
   sudo cp webhook-mcp.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable webhook-mcp
   sudo systemctl start webhook-mcp
   ```

5. **Docker Deployment**: Alternatively, you can containerize the service:

   a. Create a Dockerfile:
   ```Dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   COPY webhook_server.py .
   
   ENV WEBHOOK_URL=https://your-webhook-url.com/endpoint
   
   CMD ["python", "webhook_server.py"]
   ```

   b. Build and run the Docker container:
   ```bash
   docker build -t webhook-mcp .
   docker run -d --name webhook-mcp webhook-mcp
   ```

## Usage in Windsurf

When using this MCP server with Windsurf IDE, the AI assistant can call the webhook tool using:

```xml
<function_calls>
  <invoke name="mcp2_send_webhook">
    <parameter name="payload">{"message": "Hello from Windsurf!", "data": {"key": "value"}}</parameter>
  </invoke>
</function_calls>
```

## Troubleshooting

- **Config File Not Found**: Ensure the config file path is correct for your environment
- **Webhook URL Not Configured**: Check that the WEBHOOK_URL is properly set in your config or environment variables
- **Connection Errors**: Verify that the webhook URL is accessible from your server
- **Permission Issues**: Ensure the service has proper permissions to read the config file and execute the script
