#!/usr/bin/env python3
"""
Test real-time weather functionality
"""

from weather_agent.agent import get_weather, get_current_time, get_weather_forecast

def test_real_weather():
    print("🌍 Testing Real-Time Weather Data")
    print("=" * 40)
    
    cities = ['New York', 'London', 'Tokyo', 'Paris']
    
    for city in cities:
        print(f"\n📍 {city}:")
        result = get_weather(city)
        if result['status'] == 'success':
            print(f"✅ {result['report']}")
        else:
            print(f"❌ {result['error_message']}")
    
    print(f"\n🕐 Current time in Tokyo:")
    time_result = get_current_time('Tokyo')
    if time_result['status'] == 'success':
        print(f"✅ {time_result['report']}")
    
    print(f"\n📅 3-day forecast for London:")
    forecast_result = get_weather_forecast('London', 3)
    if forecast_result['status'] == 'success':
        print(f"✅ {forecast_result['report']}")

if __name__ == "__main__":
    test_real_weather()
