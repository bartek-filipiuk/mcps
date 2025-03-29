#!/usr/bin/env node

const { FastMCP } = require('mcp');
const axios = require('axios');
const fs = require('fs');
const path = require('path');
const os = require('os');

// Initialize FastMCP server with proper name
const mcp = new FastMCP('webhook-mcp-server');

/**
 * Read the MCP config file to get environment variables
 */
function readConfig() {
  try {
    // Allow config path to be specified via environment variable
    const configPath = process.env.CONFIG_PATH || path.join(os.homedir(), '.codeium', 'windsurf', 'mcp_config.json');
    
    if (fs.existsSync(configPath)) {
      const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
      
      // Extract environment variables from config
      if (config.mcpServers) {
        for (const [serverName, serverConfig] of Object.entries(config.mcpServers)) {
          if (serverName === 'webhook-mcp-server' && serverConfig.env) {
            return serverConfig.env;
          }
        }
      }
    }
    return {};
  } catch (e) {
    console.error(`Error reading config file: ${e.message}`);
    return {};
  }
}

/**
 * Send a POST request to the configured webhook URL
 * @param {Object} payload - Dictionary containing the data to send
 * @returns {Promise<Object>} - Response details
 */
async function sendWebhook(payload) {
  // Get environment variables from config or process.env
  const envVars = readConfig();
  const webhookUrl = process.env.WEBHOOK_URL || envVars.WEBHOOK_URL;
  
  if (!webhookUrl) {
    return { error: 'WEBHOOK_URL not configured in environment variables' };
  }
  
  try {
    // Ensure payload is properly formatted as JSON
    const jsonPayload = JSON.stringify(payload);
    
    // Set headers for JSON content
    const headers = { 'Content-Type': 'application/json' };
    
    // Send POST request to webhook URL
    const response = await axios.post(webhookUrl, payload, { headers });
    
    return {
      status_code: response.status,
      headers: response.headers,
      content: response.data
    };
  } catch (e) {
    return { error: `Error sending webhook: ${e.message}` };
  }
}

// Register the tool
mcp.tool('send_webhook', sendWebhook);

// Start the server with stdio transport
mcp.run({ transport: 'stdio' });

console.log('Webhook MCP Server started');
