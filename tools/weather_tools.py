"""
Weather-specific tools for OpenWeatherMap API integration
"""
import json
import asyncio
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.client import client
from core.config import config

def run_async_tool(async_func, *args, **kwargs):
    """Synchronous wrapper for async tools"""
    try:
        import concurrent.futures
        
        try:
            loop = asyncio.get_running_loop()
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, async_func(*args, **kwargs))
                result = future.result(timeout=30)
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

async def get_current_weather_async(city: str, units: str = "metric") -> Dict[str, Any]:
    """Get current weather for a city"""
    try:
        print(f"🌤️ Getting current weather for {city}...")
        
        params = {
            "q": city,
            "units": units,
            "appid": config.api.api_key
        }
        
        response = await client.get("/weather", params=params)
        
        # Extract relevant data
        weather_data = {
            "city": response.get("name", city),
            "country": response.get("sys", {}).get("country", "Unknown"),
            "temperature": response.get("main", {}).get("temp", 0),
            "feels_like": response.get("main", {}).get("feels_like", 0),
            "humidity": response.get("main", {}).get("humidity", 0),
            "pressure": response.get("main", {}).get("pressure", 0),
            "description": response.get("weather", [{}])[0].get("description", "Unknown"),
            "wind_speed": response.get("wind", {}).get("speed", 0),
            "wind_direction": response.get("wind", {}).get("deg", 0),
            "visibility": response.get("visibility", 0) / 1000,  # Convert to km
            "units": units,
            "timestamp": datetime.now().isoformat()
        }
        
        return {
            "status": "success",
            "data": weather_data,
            "raw_response": response
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to get weather for {city}: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

async def get_weather_forecast_async(city: str, days: int = 5, units: str = "metric") -> Dict[str, Any]:
    """Get weather forecast for a city"""
    try:
        print(f"📅 Getting {days}-day forecast for {city}...")
        
        params = {
            "q": city,
            "cnt": days * 8,  # 8 forecasts per day (every 3 hours)
            "units": units,
            "appid": config.api.api_key
        }
        
        response = await client.get("/forecast", params=params)
        
        # Process forecast data
        forecasts = []
        for item in response.get("list", []):
            forecast = {
                "datetime": item.get("dt_txt", ""),
                "temperature": item.get("main", {}).get("temp", 0),
                "feels_like": item.get("main", {}).get("feels_like", 0),
                "humidity": item.get("main", {}).get("humidity", 0),
                "description": item.get("weather", [{}])[0].get("description", "Unknown"),
                "wind_speed": item.get("wind", {}).get("speed", 0),
                "precipitation": item.get("rain", {}).get("3h", 0) + item.get("snow", {}).get("3h", 0)
            }
            forecasts.append(forecast)
        
        return {
            "status": "success",
            "city": response.get("city", {}).get("name", city),
            "country": response.get("city", {}).get("country", "Unknown"),
            "forecasts": forecasts[:days*8],  # Limit to requested days
            "units": units,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to get forecast for {city}: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

async def search_cities_async(query: str, limit: int = 5) -> Dict[str, Any]:
    """Search for cities by name"""
    try:
        print(f"🔍 Searching cities matching '{query}'...")
        
        params = {
            "q": query,
            "limit": limit,
            "appid": config.api.api_key
        }
        
        response = await client.get("/find", params=params)
        
        cities = []
        for item in response.get("list", []):
            city = {
                "name": item.get("name", ""),
                "country": item.get("sys", {}).get("country", ""),
                "state": item.get("sys", {}).get("state", ""),
                "lat": item.get("coord", {}).get("lat", 0),
                "lon": item.get("coord", {}).get("lon", 0),
                "population": item.get("population", 0)
            }
            cities.append(city)
        
        return {
            "status": "success",
            "query": query,
            "cities": cities,
            "count": len(cities),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to search cities: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

def register_weather_tools(mcp):
    """Register weather-specific tools with FastMCP"""
    
    @mcp.tool()
    def get_current_weather(city: str, units: str = "metric") -> str:
        """
        Get current weather conditions for a specific city.
        
        Args:
            city: Name of the city (e.g., "London", "New York", "Tokyo")
            units: Temperature units - "metric" (Celsius), "imperial" (Fahrenheit), or "kelvin"
        
        Returns:
            JSON string with current weather data including temperature, humidity, wind, etc.
        """
        if not city:
            error_result = {"status": "error", "message": "City name is required"}
            return json.dumps(error_result, indent=2)
            
        result = run_async_tool(get_current_weather_async, city, units)
        return json.dumps(result, indent=2)
    
    @mcp.tool()
    def get_weather_forecast(city: str, days: int = 5, units: str = "metric") -> str:
        """
        Get weather forecast for a specific city.
        
        Args:
            city: Name of the city (e.g., "London", "New York", "Tokyo")
            days: Number of days to forecast (1-5, default: 5)
            units: Temperature units - "metric" (Celsius), "imperial" (Fahrenheit), or "kelvin"
        
        Returns:
            JSON string with weather forecast data for the specified period
        """
        if not city:
            error_result = {"status": "error", "message": "City name is required"}
            return json.dumps(error_result, indent=2)
            
        if days < 1 or days > 5:
            error_result = {"status": "error", "message": "Days must be between 1 and 5"}
            return json.dumps(error_result, indent=2)
            
        result = run_async_tool(get_weather_forecast_async, city, days, units)
        return json.dumps(result, indent=2)
    
    @mcp.tool()
    def search_cities(query: str, limit: int = 5) -> str:
        """
        Search for cities by name to find the correct city for weather queries.
        
        Args:
            query: City name or part of city name to search for
            limit: Maximum number of cities to return (1-10, default: 5)
        
        Returns:
            JSON string with list of matching cities and their details
        """
        if not query:
            error_result = {"status": "error", "message": "Search query is required"}
            return json.dumps(error_result, indent=2)
            
        if limit < 1 or limit > 10:
            error_result = {"status": "error", "message": "Limit must be between 1 and 10"}
            return json.dumps(error_result, indent=2)
            
        result = run_async_tool(search_cities_async, query, limit)
        return json.dumps(result, indent=2)

    print("🌤️ Weather tools registered: get_current_weather, get_weather_forecast, search_cities")