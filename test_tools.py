#!/usr/bin/env python3
"""
Test script for weather MCP tools
"""
import asyncio
import json
from tools.weather_tools import (
    get_current_weather_async, 
    get_weather_forecast_async, 
    search_cities_async
)

async def test_all_tools():
    """Test all weather tools"""
    print("🧪 Testing Weather MCP Tools")
    print("=" * 50)
    
    # Test 1: Current Weather
    print("\n1️⃣ Testing Current Weather for London...")
    weather = await get_current_weather_async("London", "metric")
    print(f"Status: {weather['status']}")
    if weather['status'] == 'success':
        data = weather['data']
        print(f"🌤️ {data['city']}, {data['country']}")
        print(f"🌡️ Temperature: {data['temperature']}°C")
        print(f"📝 Description: {data['description']}")
        print(f"💨 Wind: {data['wind_speed']} m/s")
    else:
        print(f"❌ Error: {weather['message']}")
    
    # Test 2: Weather Forecast
    print("\n2️⃣ Testing 3-day Forecast for Tokyo...")
    forecast = await get_weather_forecast_async("Tokyo", 3, "metric")
    print(f"Status: {forecast['status']}")
    if forecast['status'] == 'success':
        print(f"🗾 {forecast['city']}, {forecast['country']}")
        print(f"📅 Forecasts: {len(forecast['forecasts'])}")
        # Show first forecast
        if forecast['forecasts']:
            first = forecast['forecasts'][0]
            print(f"📍 Next: {first['datetime']} - {first['temperature']}°C, {first['description']}")
    else:
        print(f"❌ Error: {forecast['message']}")
    
    # Test 3: City Search  
    print("\n3️⃣ Testing City Search for 'Milan'...")
    cities = await search_cities_async("Milan", 3)
    print(f"Status: {cities['status']}")
    if cities['status'] == 'success':
        print(f"🔍 Found {cities['count']} cities:")
        for city in cities['cities'][:3]:
            print(f"   📍 {city['name']}, {city['country']} ({city['lat']}, {city['lon']})")
    else:
        print(f"❌ Error: {cities['message']}")
    
    print("\n✅ Tool testing completed!")

if __name__ == "__main__":
    asyncio.run(test_all_tools())
