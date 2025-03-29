# Deploying Webhook MCP Server

This guide explains how to deploy your webhook MCP server to a public server using GitHub as your code repository.

## 1. Create a GitHub Repository

First, set up a GitHub repository for your code:

1. Create a new repository on GitHub (e.g., "webhook-mcp-server")
2. Push your local code to the repository:

```bash
# Navigate to your project directory
cd /home/bartek/www/mcps/webhook

# Initialize git repository (if not already done)
git init

# Add your files
git add webhook_server.py requirements.txt README.md

# Commit the files
git commit -m "Initial commit of webhook MCP server"

# Add your GitHub repository as remote
git remote add origin https://github.com/yourusername/webhook-mcp-server.git

# Push to GitHub
git push -u origin main
```

## 2. Server Deployment Options

### Option 1: Deploy to a VPS or Cloud Server

1. **Set up a server** (e.g., AWS EC2, DigitalOcean Droplet, or any VPS)
2. **Clone your repository**:

```bash
# SSH into your server
ssh user@your-server-ip

# Clone your repository
git clone https://github.com/yourusername/webhook-mcp-server.git
cd webhook-mcp-server

# Install dependencies
pip install -r requirements.txt
```

3. **Modify the configuration path** in webhook_server.py:

```python
# Change this line in the read_config function
config_path = "/path/to/your/server/config.json"
```

4. **Create a configuration file** on your server:

```bash
# Create a directory for the config
mkdir -p /path/to/your/server/

# Create the config file
cat > /path/to/your/server/config.json << EOF
{
  "mcpServers": {
    "webhook-mcp-server": {
      "env": {
        "WEBHOOK_URL": "https://your-webhook-url.com/endpoint"
      }
    }
  }
}
EOF
```

5. **Set up as a systemd service**:

```bash
# Create a service file
cat > webhook-mcp.service << EOF
[Unit]
Description=Webhook MCP Server
After=network.target

[Service]
User=$(whoami)
WorkingDirectory=$(pwd)
ExecStart=$(which python3) $(pwd)/webhook_server.py
Restart=always
Environment=WEBHOOK_URL=https://your-webhook-url.com/endpoint

[Install]
WantedBy=multi-user.target
EOF

# Install and start the service
sudo cp webhook-mcp.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable webhook-mcp
sudo systemctl start webhook-mcp
```

### Option 2: Deploy Using GitHub Actions and Docker

1. **Add a Dockerfile** to your repository:

```Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY webhook_server.py .

ENV WEBHOOK_URL=https://your-webhook-url.com/endpoint

CMD ["python", "webhook_server.py"]
```

2. **Create a GitHub Actions workflow** to build and deploy your Docker image:

```yaml
# .github/workflows/docker-build.yml
name: Build and Deploy Docker Image

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Login to GitHub Container Registry
        uses: docker/login-action@v1
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Build and push
        uses: docker/build-push-action@v2
        with:
          context: .
          push: true
          tags: ghcr.io/${{ github.repository }}:latest
```

3. **Deploy the Docker container** on your server:

```bash
# Pull the image from GitHub Container Registry
docker pull ghcr.io/yourusername/webhook-mcp-server:latest

# Run the container
docker run -d --name webhook-mcp \
  -e WEBHOOK_URL=https://your-webhook-url.com/endpoint \
  ghcr.io/yourusername/webhook-mcp-server:latest
```

### Option 3: Deploy to a Serverless Platform

For a serverless approach (e.g., AWS Lambda, Google Cloud Functions):

1. **Modify the code** to work with serverless functions:

```python
# Create a new file lambda_handler.py
import json
from webhook_server import send_webhook

async def lambda_handler(event, context):
    # Parse the payload from the event
    payload = json.loads(event['body']) if 'body' in event else {}
    
    # Call the send_webhook function
    result = await send_webhook(payload)
    
    # Return the result
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
```

2. **Set up GitHub Actions** to deploy to your serverless platform of choice.

## 3. Keeping Your Server Updated

To automatically update your server when you push changes to GitHub:

1. **Set up a webhook** on your GitHub repository
2. **Create a simple update script** on your server:

```bash
#!/bin/bash
cd /path/to/webhook-mcp-server
git pull
sudo systemctl restart webhook-mcp
```

3. **Configure your server** to run this script when it receives the GitHub webhook.

## 4. Security Considerations

1. **Store sensitive information** (like the webhook URL) as environment variables or in a secure configuration store
2. **Use HTTPS** for all communications
3. **Implement authentication** if your webhook needs to be protected
4. **Regularly update** dependencies to patch security vulnerabilities

## 5. Troubleshooting

- **Config File Not Found**: Ensure the config file path is correct for your environment
- **Webhook URL Not Configured**: Check that the WEBHOOK_URL is properly set in your config or environment variables
- **Connection Errors**: Verify that the webhook URL is accessible from your server
- **Permission Issues**: Ensure the service has proper permissions to read the config file and execute the script
