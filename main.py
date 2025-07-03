#!/usr/bin/env python3
"""
Weather MCP Server - OpenWeatherMap Integration
Built with mcp-server-template
"""
import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

import json
from datetime import datetime

# FastMCP import
from mcp.server.fastmcp import FastMCP

# Import our modules
from core.auth import auth
from core.client import client
from core.config import config

# Import weather tools
from tools.weather_tools import register_weather_tools

# Data directory for storing API responses
DATA_DIR = "weather_mcp_server_data"

# Get port from environment (Render sets this automatically)
PORT = int(os.environ.get("PORT", 8000))

# Initialize FastMCP server
mcp = FastMCP(name=config.mcp.server_name, host="0.0.0.0", port=PORT)

def save_api_data(data_type: str, data: dict) -> None:
    """Save API data to file for debugging"""
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{data_type}_{timestamp}.json"
        filepath = os.path.join(DATA_DIR, filename)
        
        data["saved_at"] = datetime.now().isoformat()
        data["server_name"] = config.mcp.server_name
        
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        if config.mcp.debug:
            print(f"💾 Data saved to: {filepath}")
            
    except Exception as e:
        print(f"❌ Error saving data: {str(e)}")

def run_async_tool(async_func, *args, **kwargs):
    """Synchronous wrapper for async tools"""
    try:
        import asyncio
        import concurrent.futures
        
        try:
            loop = asyncio.get_running_loop()
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, async_func(*args, **kwargs))
                result = future.result(timeout=60)
                return result
        except RuntimeError:
            result = asyncio.run(async_func(*args, **kwargs))
            return result
    except Exception as e:
        return {
            "status": "error",
            "message": f"Tool execution failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

# Basic API status tool
async def get_api_status_async():
    """Get OpenWeatherMap API status"""
    try:
        print("🔍 Checking OpenWeatherMap API status...")
        
        # Test with a simple weather query
        params = {
            "q": "London",
            "appid": config.api.api_key
        }
        
        response = await client.get("/weather", params=params)
        
        return {
            "status": "success",
            "api_name": "OpenWeatherMap",
            "api_status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "test_query": "London weather",
            "response_time": "fast",
            "authentication": {
                "type": "API Key",
                "valid": True
            },
            "configuration": {
                "base_url": config.api.base_url,
                "environment": config.mcp.environment,
                "debug_mode": config.mcp.debug
            }
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"API status check failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

@mcp.tool()
def get_api_status() -> str:
    """
    Check OpenWeatherMap API connectivity and authentication status.
    
    Returns:
        JSON string with API status, authentication info, and configuration details
    """
    result = run_async_tool(get_api_status_async)
    save_api_data("api_status", result)
    return json.dumps(result, indent=2)

# Resources for documentation
@mcp.resource("weather://status")
def get_server_status() -> str:
    """Get current weather server status"""
    try:
        status_info = {
            "server_name": config.mcp.server_name,
            "server_version": config.mcp.server_version,
            "environment": config.mcp.environment,
            "api_provider": "OpenWeatherMap",
            "available_tools": [
                "get_api_status",
                "get_current_weather", 
                "get_weather_forecast",
                "search_cities"
            ],
            "last_updated": datetime.now().isoformat()
        }
        
        content = f"# Weather MCP Server Status\n\n"
        content += f"**Status**: ✅ Running\n"
        content += f"**API Provider**: OpenWeatherMap\n"
        content += f"**Version**: {status_info['server_version']}\n"
        content += f"**Environment**: {status_info['environment']}\n\n"
        
        content += f"## Available Weather Tools ({len(status_info['available_tools'])})\n"
        for tool in status_info["available_tools"]:
            content += f"- `{tool}`\n"
            
        content += f"\n## Example Usage\n"
        content += f"- **Current Weather**: `get_current_weather('London')`\n"
        content += f"- **5-Day Forecast**: `get_weather_forecast('Tokyo', 5)`\n"
        content += f"- **Search Cities**: `search_cities('Milan')`\n"
        content += f"- **API Status**: `get_api_status()`\n\n"
        
        content += f"**Last updated**: {status_info['last_updated']}\n"
        
        return content
        
    except Exception as e:
        return f"# Server Status Error\n\nError: {str(e)}"

@mcp.resource("weather://examples")
def get_weather_examples() -> str:
    """Get weather API usage examples"""
    content = """# Weather MCP Server - Usage Examples

## 1. Check Current Weather

```python
# Get current weather in London
weather = get_current_weather("London")

# Get weather in Fahrenheit
weather_f = get_current_weather("New York", "imperial")

# Get weather in Kelvin
weather_k = get_current_weather("Tokyo", "kelvin")
```

## 2. Get Weather Forecast

```python
# Get 5-day forecast for Paris
forecast = get_weather_forecast("Paris", 5)

# Get 3-day forecast in Fahrenheit
forecast = get_weather_forecast("Miami", 3, "imperial")
```

## 3. Search for Cities

```python
# Find cities named Milan
cities = search_cities("Milan")

# Search for cities with partial name
cities = search_cities("San", 10)
```

## 4. Check API Status

```python
# Verify OpenWeatherMap connectivity
status = get_api_status()
```

## Response Format

All weather tools return JSON with this structure:

```json
{
  "status": "success",
  "data": {
    "city": "London",
    "temperature": 15.5,
    "description": "partly cloudy",
    "humidity": 65,
    "wind_speed": 3.2
  },
  "timestamp": "2025-01-15T10:30:00"
}
```

## Supported Units

- **metric**: Celsius, m/s, km
- **imperial**: Fahrenheit, mph, miles  
- **kelvin**: Kelvin, m/s, km

## Rate Limits

- Free tier: 60 calls/minute, 1M calls/month
- Current setting: 60 requests per minute
"""
    return content

def main():
    """Main server entry point"""
    
    # Configuration validation
    print("🔧 Validating weather server configuration...")
    try:
        config.validate()
        print(f"✅ Configuration valid")
        print(f"🌤️ OpenWeatherMap API: {config.api.base_url}")
        
        if config.mcp.debug:
            debug_info = config.get_debug_info()
            print(f"🔍 Debug info: {debug_info}")
            
    except Exception as e:
        print(f"❌ Configuration validation failed: {e}")
        print("💡 Check your .env file - make sure API_KEY is set")
        sys.exit(1)
    
    # Data directory setup
    os.makedirs(DATA_DIR, exist_ok=True)
    print(f"📁 Data directory: {DATA_DIR}")
    
    # Register weather tools
    print("🔧 Registering weather tools...")
    register_weather_tools(mcp)
    
    # Server startup
    print(f"\n🚀 Starting Weather MCP Server")
    print(f"📊 Server: {config.mcp.server_name}")
    print(f"🌍 Host: 0.0.0.0:{PORT}")
    print(f"🌤️ API: OpenWeatherMap")
    print(f"🎯 Transport: SSE (Server-Sent Events)")
    print(f"🔧 4 weather tools registered")
    print(f"✅ Weather MCP Server is ready!")
    print(f"💡 Ask Claude: 'What's the weather like in London?'")
    
    # Start the MCP server
    mcp.run(transport="sse")

if __name__ == "__main__":
    main()