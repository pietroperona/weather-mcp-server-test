# Weather MCP Server Documentation

MCP server for external API integration with Render.com deployment

**Generated from**: [mcp-server-template](https://github.com/pietroperona/mcp-server-template)  
**Author**: Pietro <you@example.com>  
**Version**: 0.1.0  
**API Type**: REST API  
**Authentication**: API Key  

## 📚 Documentation Index

- [🚀 Quick Start Guide](quick-start.md) - Get up and running in 5 minutes
- [⚙️ Configuration Guide](configuration.md) - Complete configuration reference
- [🔧 API Integration](api-integration.md) - How to customize for your API
- [🛠️ Development Guide](development.md) - Local development setup
- [🚀 Deployment Guide](deployment.md) - Deploy to Render.com and Docker
- [🔍 Troubleshooting](troubleshooting.md) - Common issues and solutions
- [📖 API Reference](api-reference.md) - Complete tool reference

## 🎯 What This Project Does

This MCP (Model Context Protocol) server provides Claude AI with tools to interact with REST API APIs. It includes:

✅ **Authentication** - API Key support  
✅ **CRUD Operations** - Create, Read, Update, Delete resources  
✅ **Error Handling** - Robust error handling and retries  
✅ **Rate Limiting** - Automatic rate limit management  
✅ **Production Ready** - One-click Render.com deployment  

## 🚀 Quick Start

1. **Configure API credentials** in `.env`
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Run server**: `python main.py`
4. **Test tools**: Server runs on `http://localhost:8000`

## 🔧 Available Tools

- `get_api_status` - Check API connectivity and authentication
- `list_resources` - List available resources with pagination
- `get_resource_by_id` - Get detailed resource information
- `create_resource` - Create new resources
- `update_resource` - Update existing resources  
- `delete_resource` - Delete resources

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/pietroperona/weather-mcp-server/issues)
- **Discussions**: [GitHub Discussions](https://github.com/pietroperona/weather-mcp-server/discussions)
- **Email**: you@example.com

---

**Generated from [mcp-server-template](https://github.com/pietroperona/mcp-server-template)** 🍪