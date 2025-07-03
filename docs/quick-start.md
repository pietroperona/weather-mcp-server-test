# 🚀 Quick Start Guide

Get Weather MCP Server running in 5 minutes!

## 📋 Prerequisites

- Python 3.11+
- REST API API access
- Valid API key
## ⚡ 5-Minute Setup

### 1. Clone & Install
```bash
git clone https://github.com/pietroperona/weather-mcp-server.git
cd weather-mcp-server
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your credentials
```

**Required variables:**
```bash
API_BASE_URL=https://your-api.com
API_KEY=your_api_key_here
```

### 3. Test Connection
```bash
python -c "
import asyncio
from core.auth import test_authentication
asyncio.run(test_authentication())
"
```

### 4. Start Server
```bash
python main.py
```

🎉 **Server running at**: `http://localhost:8000`

## 🧪 Test Your Setup

### Test API Status
```bash
curl http://localhost:8000/tools/get_api_status
```

### Test Resource Listing
```bash
curl "http://localhost:8000/tools/list_resources?resource_type=users&limit=5"
```

## 🔧 Configure Claude Desktop

Add to your Claude Desktop MCP configuration:

```json
{
  "mcpServers": {
    "weather-mcp-server": {
      "command": "python",
      "args": ["weather-mcp-server/main.py"],
      "cwd": "weather-mcp-server"
    }
  }
}
```

## ✅ Verify Tools in Claude

Ask Claude: *"What tools do you have available?"*

You should see:
- ✅ get_api_status
- ✅ list_resources  
- ✅ get_resource_by_id
- ✅ create_resource
- ✅ update_resource
- ✅ delete_resource

## 🚀 Deploy to Production

**One-click deploy to Render.com:**

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=pietroperona/weather-mcp-server)

See [Deployment Guide](deployment.md) for detailed instructions.

## 🆘 Having Issues?

### Quick Troubleshooting

**Authentication Failed?**
- Verify credentials in `.env`
- Check API endpoint is correct
- Run `python core/auth.py` to test auth

**Connection Failed?**
- Verify `API_BASE_URL` is correct
- Check internet connection
- Try `python core/client.py` to test connectivity

**Tools Not Available?**
- Check MCP configuration in Claude Desktop
- Restart Claude Desktop after config changes
- Verify server is running on correct port

**Still stuck?** Check the [full troubleshooting guide](troubleshooting.md).

## 📚 Next Steps

- [⚙️ Configuration Guide](configuration.md) - Detailed configuration options
- [🔧 API Integration](api-integration.md) - Customize for your specific API
- [🛠️ Development Guide](development.md) - Local development workflow

---

**Need help?** Open an issue on [GitHub](https://github.com/pietroperona/weather-mcp-server/issues) 🆘