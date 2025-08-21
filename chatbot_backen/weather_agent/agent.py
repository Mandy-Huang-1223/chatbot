import datetime
import requests
import os
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from dotenv import load_dotenv

# Load environment variables from the main .env file
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city using OpenWeatherMap API.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    try:
        # Get API key from environment variable
        api_key = os.environ.get("OPENWEATHER_API_KEY")
        
        if not api_key:
            # Fallback to mock data if no API key is provided
            if city.lower() in ["new york", "london", "paris", "tokyo"]:
                mock_data = {
                    "new york": "Sunny with a temperature of 25°C (77°F). Light wind from the southwest.",
                    "london": "Cloudy with occasional rain, 18°C (64°F). Moderate wind from the west.",
                    "paris": "Partly cloudy, 22°C (72°F). Light breeze from the north.",
                    "tokyo": "Clear skies, 28°C (82°F). High humidity with light wind."
                }
                return {
                    "status": "success",
                    "report": f"The weather in {city.title()} is {mock_data[city.lower()]}",
                }
            else:
                return {
                    "status": "error",
                    "error_message": f"Weather information for '{city}' is not available. Please try New York, London, Paris, or Tokyo.",
                }
        
        # Make API call to OpenWeatherMap
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric"
        }
        
        response = requests.get(base_url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            weather_desc = data['weather'][0]['description'].title()
            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            
            report = (
                f"The weather in {city.title()} is {weather_desc} with a temperature of "
                f"{temp}°C ({temp * 9/5 + 32:.1f}°F). Feels like {feels_like}°C. "
                f"Humidity: {humidity}%. Wind speed: {wind_speed} m/s."
            )
            
            return {
                "status": "success",
                "report": report,
            }
        elif response.status_code == 404:
            return {
                "status": "error",
                "error_message": f"City '{city}' not found. Please check the spelling and try again.",
            }
        else:
            return {
                "status": "error",
                "error_message": f"Unable to fetch weather data for '{city}'. Please try again later.",
            }
            
    except requests.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Network error while fetching weather data: {str(e)}",
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error retrieving weather data: {str(e)}",
        }


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """
    
    # Extended city timezone mapping
    city_timezones = {
        "new york": "America/New_York",
        "london": "Europe/London",
        "paris": "Europe/Paris",
        "tokyo": "Asia/Tokyo",
        "los angeles": "America/Los_Angeles",
        "chicago": "America/Chicago",
        "sydney": "Australia/Sydney",
        "moscow": "Europe/Moscow",
        "beijing": "Asia/Shanghai",
        "mumbai": "Asia/Kolkata",
        "dubai": "Asia/Dubai",
        "singapore": "Asia/Singapore",
        "berlin": "Europe/Berlin",
        "rome": "Europe/Rome",
        "madrid": "Europe/Madrid",
        "toronto": "America/Toronto",
        "vancouver": "America/Vancouver",
        "mexico city": "America/Mexico_City",
        "sao paulo": "America/Sao_Paulo",
        "buenos aires": "America/Argentina/Buenos_Aires",
    }
    
    city_lower = city.lower()
    
    if city_lower in city_timezones:
        tz_identifier = city_timezones[city_lower]
    else:
        return {
            "status": "error",
            "error_message": (
                f"Sorry, I don't have timezone information for {city}. "
                f"Supported cities: {', '.join([c.title() for c in city_timezones.keys()])}"
            ),
        }

    try:
        tz = ZoneInfo(tz_identifier)
        now = datetime.datetime.now(tz)
        report = (
            f'The current time in {city.title()} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
        )
        
        return {"status": "success", "report": report}
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error getting time for {city}: {str(e)}",
        }


def get_weather_forecast(city: str, days: int = 3) -> dict:
    """Gets weather forecast for a specified city.

    Args:
        city (str): The name of the city for which to retrieve the forecast.
        days (int): Number of days for forecast (1-5, default 3).

    Returns:
        dict: status and result or error msg.
    """
    try:
        # Validate days parameter
        if days < 1 or days > 5:
            days = 3
            
        api_key = os.environ.get("OPENWEATHER_API_KEY")
        
        if not api_key:
            # Mock forecast data
            mock_forecasts = {
                "new york": [
                    "Tomorrow: Partly cloudy, 24°C (75°F)",
                    "Day 2: Sunny, 27°C (81°F)", 
                    "Day 3: Light rain, 21°C (70°F)"
                ],
                "london": [
                    "Tomorrow: Overcast, 17°C (63°F)",
                    "Day 2: Light rain, 15°C (59°F)",
                    "Day 3: Partly cloudy, 19°C (66°F)"
                ]
            }
            
            if city.lower() in mock_forecasts:
                forecast_list = mock_forecasts[city.lower()][:days]
                forecast_text = "\n".join(forecast_list)
                return {
                    "status": "success",
                    "report": f"Weather forecast for {city.title()}:\n{forecast_text}",
                }
            else:
                return {
                    "status": "error",
                    "error_message": f"Forecast data for '{city}' is not available in demo mode.",
                }
        
        # If API key is available, make real API call
        base_url = "http://api.openweathermap.org/data/2.5/forecast"
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric",
            "cnt": days * 8  # 8 forecasts per day (every 3 hours)
        }
        
        response = requests.get(base_url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            forecasts = []
            
            # Group forecasts by day
            for i in range(0, min(len(data['list']), days * 8), 8):
                forecast = data['list'][i]
                date = datetime.datetime.fromtimestamp(forecast['dt']).strftime('%A, %B %d')
                temp = forecast['main']['temp']
                desc = forecast['weather'][0]['description'].title()
                forecasts.append(f"{date}: {desc}, {temp}°C ({temp * 9/5 + 32:.1f}°F)")
            
            forecast_text = "\n".join(forecasts)
            return {
                "status": "success", 
                "report": f"Weather forecast for {city.title()}:\n{forecast_text}",
            }
        else:
            return {
                "status": "error",
                "error_message": f"Unable to fetch forecast data for '{city}'.",
            }
            
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error retrieving forecast data: {str(e)}",
        }


# Create the weather agent
weather_agent = Agent(
    name="weather_time_agent",
    model="gemini-2.0-flash",
    description=(
        "Agent to answer questions about the time, weather, and weather forecasts in cities worldwide."
    ),
    instruction=(
        "You are a helpful agent who can answer user questions about the time, current weather, "
        "and weather forecasts in cities around the world. You can provide current weather conditions, "
        "time information, and multi-day weather forecasts. Always be friendly and informative in your responses."
    ),
    tools=[get_weather, get_current_time, get_weather_forecast],
)
