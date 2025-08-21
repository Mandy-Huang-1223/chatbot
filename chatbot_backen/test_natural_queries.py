#!/usr/bin/env python3
"""
Test natural weather queries
"""

from chatbot_api import handle_weather_query

def test_natural_queries():
    print("🌤️ Testing Natural Weather Queries")
    print("=" * 50)
    
    test_queries = [
        "Is it raining in London?",
        "Is it sunny in Paris?", 
        "Is it cold in New York?",
        "Is it hot in Tokyo?",
        "What's the weather in London?",
        "How's the weather in Paris?",
        "Weather in New York",
        "Temperature in Tokyo",
        "Is it windy in Chicago?",
        "Is it cloudy in Berlin?"
    ]
    
    for query in test_queries:
        print(f"\n❓ Query: '{query}'")
        result = handle_weather_query(query)
        
        if result:
            if result.get('status') == 'success':
                # Extract just the key weather info for easier reading
                report = result['report']
                if 'with a temperature of' in report:
                    weather_desc = report.split(' with a temperature of')[0].split(' is ')[-1]
                    temp_info = report.split(' with a temperature of')[1].split('.')[0]
                    print(f"✅ {weather_desc}, {temp_info}")
                else:
                    print(f"✅ {report}")
            else:
                print(f"❌ {result.get('error_message', 'Unknown error')}")
        else:
            print("❌ Not detected as weather query")

if __name__ == "__main__":
    test_natural_queries()
