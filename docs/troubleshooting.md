# 🔍 Troubleshooting Guide

Common issues and solutions for Weather MCP Server.

## 🚨 Quick Diagnostics

Run these commands to quickly identify issues:

### 1. Test Configuration
```bash
python -c "
from core.config import config
try:
    config.validate()
    print('✅ Configuration valid')
except Exception as e:
    print(f'❌ Configuration error: {e}')
"
```

### 2. Test Authentication
```bash
python core/auth.py
```

### 3. Test API Connectivity
```bash
python core/client.py
```

### 4. Test MCP Server
```bash
python main.py
# Look for startup messages and errors
```

## 🔐 Authentication Issues

### ❌ "Authentication failed" / "401 Unauthorized"

**Possible Causes:**
- Invalid or expired API key
- Wrong API key header name
- API key doesn't have required permissions

**Solutions:**
1. **Verify API Key:**
   ```bash
   # Check your API key is set
   echo $API_KEY
   # Or check in .env file
   grep API_KEY .env
   ```

2. **Test API Key directly:**
   ```bash
   curl -H "X-API-Key: YOUR_API_KEY" https://api.openweathermap.org/data/2.5/endpoint
   ```

3. **Check API Key Header:**
   ```bash
   # Some APIs use different header names
   API_KEY_HEADER=Authorization  # Try this
   API_KEY_HEADER=X-API-Token    # Or this
   ```

4. **Check API Permissions:**
   - Verify API key/token has required scopes
   - Check rate limits aren't exceeded
   - Ensure account is in good standing

## 🌐 Connection Issues

### ❌ "Connection failed" / "Network error"

**Possible Causes:**
- Wrong API base URL
- Network connectivity issues
- API service is down
- Firewall blocking requests

**Solutions:**

1. **Verify API URL:**
   ```bash
   # Test URL accessibility
   curl -I https://api.openweathermap.org/data/2.5
   
   # Check DNS resolution
   nslookup api.example.com
   ```

2. **Check Network Connectivity:**
   ```bash
   # Test internet connection
   ping google.com
   
   # Test specific host
   ping api.example.com
   ```

3. **Verify API Status:**
   - Check API provider's status page
   - Look for maintenance announcements
   - Try different endpoints

4. **Firewall/Proxy Issues:**
   ```bash
   # Try with proxy if needed
   export HTTP_PROXY=http://proxy.company.com:8080
   export HTTPS_PROXY=http://proxy.company.com:8080
   ```

### ❌ "Request timeout" / "Timeout error"

**Solutions:**

1. **Increase Timeout:**
   ```bash
   API_TIMEOUT=60  # Increase to 60 seconds
   ```

2. **Check API Response Time:**
   ```bash
   # Test API response time
   time curl https://api.openweathermap.org/data/2.5/endpoint
   ```

3. **Retry Configuration:**
   ```python
   # Modify retry settings in core/client.py
   max_retries = 5
   base_delay = 2.0
   ```

## 📊 API Response Issues

### ❌ "404 Not Found" / "Resource does not exist"

**Solutions:**

1. **Verify Endpoint:**
   ```bash
   # Check API documentation for correct endpoints
   # Common patterns:
   /api/v1/users          # REST standard
   /v1/users             # Version prefix
   /users                # Simple
   ```

2. **Check Resource ID Format:**
   ```bash
   # Different ID formats:
   "123"                 # Numeric
   "user_123"            # Prefixed
   "uuid-string"         # UUID
   ```

3. **Verify Resource Exists:**
   ```bash
   # List resources first
   python -c "
   import asyncio
   from tools.example_tools import list_resources_async
   result = asyncio.run(list_resources_async('users', 5, 0))
   print(result)
   "
   ```

### ❌ "400 Bad Request" / "Invalid data"

**Solutions:**

1. **Check JSON Format:**
   ```python
   # Validate JSON before sending
   import json
   data = {"name": "John", "email": "john@example.com"}
   json_string = json.dumps(data)
   print(json_string)  # Should be valid JSON
   ```

2. **Verify Required Fields:**
   - Check API documentation for required fields
   - Ensure data types match (string, number, boolean)
   - Check field name spelling

3. **Test with Minimal Data:**
   ```python
   # Start with minimal required fields
   minimal_data = {"name": "Test User"}
   # Add fields one by one to identify the issue
   ```

### ❌ "429 Too Many Requests" / "Rate limit exceeded"

**Solutions:**

1. **Check Rate Limit Settings:**
   ```bash
   # Reduce request frequency
   RATE_LIMIT_REQUESTS=50    # Lower limit
   RATE_LIMIT_WINDOW=3600    # Per hour
   ```

2. **Wait and Retry:**
   ```python
   # Automatic backoff is built-in
   # Wait for rate limit window to reset
   import time
   time.sleep(60)  # Wait 1 minute
   ```

3. **Monitor Usage:**
   ```bash
   # Enable debug mode to see request frequency
   DEBUG=true python main.py
   ```

4. **Contact API Provider:**
   - Request higher rate limits
   - Understand your current limits
   - Check if you have a premium plan

## 🔧 MCP Server Issues

### ❌ "Tools not available in Claude Desktop"

**Solutions:**

1. **Check MCP Configuration:**
   ```json
   // In Claude Desktop settings
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

2. **Verify Server is Running:**
   ```bash
   # Check if server starts without errors
   python main.py
   # Look for "✅ Weather MCP Server is ready!"
   ```

3. **Check Tool Registration:**
   ```bash
   # Verify tools are registered
   python -c "
   from tools import get_available_tools
   tools = get_available_tools()
   print(f'Available tools: {tools}')
   "
   ```

4. **Restart Claude Desktop:**
   - Close Claude Desktop completely
   - Wait 10 seconds
   - Restart Claude Desktop
   - Tools should appear in new conversation

### ❌ "Server won't start" / "Import errors"

**Solutions:**

1. **Check Python Version:**
   ```bash
   python --version
   # Should be 3.11+
   ```

2. **Verify Dependencies:**
   ```bash
   # Reinstall dependencies
   pip install -r requirements.txt
   
   # Check specific imports
   python -c "import fastmcp; print('✅ FastMCP installed')"
   python -c "import aiohttp; print('✅ aiohttp installed')"
   ```

3. **Check Import Paths:**
   ```bash
   # Verify Python path
   python -c "
   import sys
   print('Python path:')
   for path in sys.path:
       print(f'  {path}')
   "
   ```

4. **Virtual Environment:**
   ```bash
   # Create clean virtual environment
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate     # Windows
   pip install -r requirements.txt
   ```

## 🐛 Development Issues

### ❌ "Module not found" errors

**Solutions:**

1. **Check Project Structure:**
   ```bash
   # Verify structure
   find . -name "*.py" -type f
   # Should show all Python files
   ```

2. **Fix Import Paths:**
   ```python
   # Add to top of files with import issues
   import sys
   from pathlib import Path
   sys.path.insert(0, str(Path(__file__).parent.parent))
   ```

3. **Use Relative Imports:**
   ```python
   # Instead of absolute imports
   from core.config import config
   # Use relative imports
   from .config import config
   ```

### ❌ "Configuration validation failed"

**Solutions:**

1. **Check .env File:**
   ```bash
   # Verify .env exists and has content
   ls -la .env
   cat .env
   ```

2. **Copy from Template:**
   ```bash
   # Start fresh from template
   cp .env.example .env
   # Edit with your values
   ```

3. **Check Variable Names:**
   ```bash
   # Ensure exact variable names (case sensitive)
   grep -E "^[A-Z_]+=.*" .env
   ```

## 🚀 Production Issues

### ❌ "Render deployment failed"

**Solutions:**

1. **Check Build Logs:**
   - Go to Render Dashboard
   - Select your service
   - View "Logs" tab
   - Look for specific error messages

2. **Verify Environment Variables:**
   ```bash
   # In Render Dashboard → Environment
   # Ensure all required variables are set
   # Check for typos in variable names
   ```

3. **Check render.yaml:**
   ```yaml
   # Verify syntax is correct
   services:
     - type: web
       name: weather-mcp-server
       env: python
   ```

4. **Test Locally First:**
   ```bash
   # Ensure it works locally before deploying
   ENVIRONMENT=production python main.py
   ```

### ❌ "Server crashes in production"

**Solutions:**

1. **Check Memory Usage:**
   ```bash
   # Reduce memory usage
   # Add to render.yaml:
   plan: starter  # Use appropriate plan
   ```

2. **Add Error Handling:**
   ```python
   # Wrap main() in try/catch
   def main():
       try:
           # Your server code
           mcp.run(transport='sse')
       except Exception as e:
           print(f"Server error: {e}")
           # Log error details
   ```

3. **Health Checks:**
   ```bash
   # Add health check endpoint
   @mcp.resource("health")
   def health_check():
       return "OK"
   ```

## 📞 Getting Help

### Still Having Issues?

1. **Enable Debug Mode:**
   ```bash
   DEBUG=true LOG_LEVEL=DEBUG python main.py
   ```

2. **Collect Information:**
   - Error messages (full stacktrace)
   - Configuration (without secrets)
   - Python version
   - Operating system
   - Steps to reproduce

3. **Get Support:**
   - **GitHub Issues**: [pietroperona/weather-mcp-server/issues](https://github.com/pietroperona/weather-mcp-server/issues)
   - **Discussions**: [pietroperona/weather-mcp-server/discussions](https://github.com/pietroperona/weather-mcp-server/discussions)
   - **Email**: you@example.com

### Issue Template

When reporting issues, include:

```markdown
**Environment:**
- OS: [macOS/Windows/Linux]
- Python version: [3.11/3.12]
- Weather MCP Server version: 0.1.0

**Configuration:**
- API Type: REST API
- Auth Type: API Key
- Environment: [development/production]

**Error Message:**
```
[Paste full error message here]
```

**Steps to Reproduce:**
1. [First step]
2. [Second step]
3. [Error occurs]

**Expected Behavior:**
[What should happen]

**Additional Context:**
[Any other relevant information]
```

---

**Still need help?** Don't hesitate to ask! 🆘