# @bartek-filipiuk/mcp-webhook

A Webhook MCP Server for sending webhook requests from AI assistants.

## Installation

```bash
npm install -g @bartek-filipiuk/mcp-webhook
```

## Usage in MCP Configuration

Add the following to your MCP configuration:

```json
{
  "mcpServers": {
    "webhook-mcp-server": {
      "command": "npx",
      "args": [
        "-y",
        "@bartek-filipiuk/mcp-webhook"
      ],
      "env": {
        "WEBHOOK_URL": "https://your-webhook-url.com/endpoint"
      }
    }
  }
}
```

## Environment Variables

- `WEBHOOK_URL` (required): The URL to send webhook requests to
- `CONFIG_PATH` (optional): Path to a custom MCP config file

## Features

- Send webhook requests with custom JSON payloads
- Compatible with any MCP client (Windsurf, Cursor, Cherry Studio, etc.)
- Simple configuration with environment variables

## GitHub Repository

This package is available on GitHub at:
https://github.com/bartek-filipiuk/mcp-webhook

## License

MIT
