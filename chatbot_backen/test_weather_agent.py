#!/usr/bin/env python3
"""
Test script for the weather agent functionality
"""

import sys
import os

# Add the parent directory to the path so we can import the weather agent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from weather_agent.agent import get_weather, get_current_time, get_weather_forecast

def test_weather_functions():
    """Test the weather agent functions."""
    print("Testing Weather Agent Functions")
    print("=" * 40)
    
    # Test weather function
    print("\n1. Testing get_weather function:")
    print("-" * 30)
    
    test_cities = ["New York", "London", "InvalidCity123"]
    
    for city in test_cities:
        print(f"\nTesting weather for: {city}")
        result = get_weather(city)
        print(f"Status: {result['status']}")
        if result['status'] == 'success':
            print(f"Report: {result['report']}")
        else:
            print(f"Error: {result['error_message']}")
    
    # Test time function
    print("\n\n2. Testing get_current_time function:")
    print("-" * 30)
    
    time_cities = ["New York", "Tokyo", "InvalidCity123"]
    
    for city in time_cities:
        print(f"\nTesting time for: {city}")
        result = get_current_time(city)
        print(f"Status: {result['status']}")
        if result['status'] == 'success':
            print(f"Report: {result['report']}")
        else:
            print(f"Error: {result['error_message']}")
    
    # Test forecast function
    print("\n\n3. Testing get_weather_forecast function:")
    print("-" * 30)
    
    forecast_cities = ["New York", "London"]
    
    for city in forecast_cities:
        print(f"\nTesting forecast for: {city}")
        result = get_weather_forecast(city, 3)
        print(f"Status: {result['status']}")
        if result['status'] == 'success':
            print(f"Report: {result['report']}")
        else:
            print(f"Error: {result['error_message']}")

if __name__ == "__main__":
    test_weather_functions()
