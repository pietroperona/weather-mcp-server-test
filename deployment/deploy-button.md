# 🚀 One-Click Deploy to Render.com

Deploy Weather MCP Server to Render.com with one click!

## Quick Deploy

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=pietroperona/weather-mcp-server)

## Manual Deploy Steps

### 1. Fork Repository
```bash
git clone https://github.com/pietroperona/weather-mcp-server.git
cd weather-mcp-server
2. Create Render Account

Go to render.com
Sign up with GitHub account
Connect your repository

3. Set Environment Variables
In Render Dashboard, set these SECRET variables:
API_KEY=your_actual_api_key_here
Required:
API_BASE_URL=https://your-api-url.com
4. Deploy

Render detects render.yaml automatically
Your server will be at: https://weather-mcp-server.onrender.com

Test Deployment
bashcurl https://weather-mcp-server.onrender.com/health
Configure Claude Desktop
json{
  "mcpServers": {
    "weather-mcp-server": {
      "command": "npx",
      "args": [
        "@modelcontextprotocol/server-fetch",
        "https://weather-mcp-server.onrender.com"
      ]
    }
  }
}
Troubleshooting

Build Failed: Check environment variables
500 Error: Check logs in Render dashboard
Tools Missing: Verify Claude Desktop MCP config


Need help? Open an issue on GitHub!

### 3. Verifica file deployment completi
```bash
ls -la
# Dovresti vedere: render.yaml, Dockerfile, deploy-button.md