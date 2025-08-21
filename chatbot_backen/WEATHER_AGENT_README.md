# Weather Agent Integration

This project now includes a Weather Agent powered by Google's Agent Development Kit (ADK) that can handle weather, time, and forecast queries.

## Features

The weather agent can handle:
- **Current Weather**: Get real-time weather information for cities worldwide
- **Current Time**: Get the current time in different cities and timezones
- **Weather Forecasts**: Get 1-5 day weather forecasts for cities

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

The weather agent uses two optional API keys:

#### Google AI Studio API Key (Required for ADK)
1. Get an API key from [Google AI Studio](https://aistudio.google.com/apikey)
2. Update `weather_agent/.env`:
   ```
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

#### OpenWeatherMap API Key (Optional)
1. Get a free API key from [OpenWeatherMap](https://openweathermap.org/api)
2. Update `weather_agent/.env`:
   ```
   OPENWEATHER_API_KEY=your_openweather_api_key_here
   ```

**Note**: If no OpenWeatherMap API key is provided, the agent will use mock weather data for demonstration purposes.

## API Endpoints

### Integrated Message Endpoint
The existing `/api/messages/gemini` endpoint now automatically detects and handles weather queries.

**POST** `/api/messages/gemini`

Example weather queries:
- "What's the weather in New York?"
- "Current time in Tokyo"
- "5-day forecast for London"

The system automatically routes weather queries to the Weather Agent while keeping all other queries with the regular Gemini AI.

### Weather Capabilities Endpoint (Optional)
**GET** `/api/messages/weather/capabilities`

Returns information about supported functions and cities for development/debugging purposes.

## Supported Cities

The weather agent supports major cities worldwide including:
- New York, Los Angeles, Chicago
- London, Paris, Berlin, Rome, Madrid
- Tokyo, Beijing, Mumbai, Singapore, Dubai
- Sydney, Toronto, Vancouver, Mexico City
- São Paulo, Buenos Aires, Moscow
- And many more...

## Example Queries

### Weather Queries
- "What's the weather like in London?"
- "Is it raining in Seattle?"
- "Temperature in Mumbai"
- "How's the weather in Tokyo today?"

### Time Queries
- "What time is it in New York?"
- "Current time in Berlin"
- "Time in Sydney right now"

### Forecast Queries
- "Weather forecast for Paris"
- "5-day forecast for London"
- "What's the weather going to be like tomorrow in Tokyo?"

## Integration with Existing Chat

The weather agent is seamlessly integrated with your existing chat system:

1. **Automatic Detection**: The system automatically detects weather-related queries
2. **Fallback to Gemini**: Non-weather queries continue to use the regular Gemini AI
3. **Message Storage**: All interactions are stored in your MongoDB database
4. **Natural Interface**: Weather responses appear as regular chat messages - no special UI needed

## Testing

Run the test script to verify functionality:

```bash
python test_weather_agent.py
```

## Architecture

```
chatbot_backend/
├── weather_agent/
│   ├── __init__.py
│   ├── agent.py          # Weather agent implementation
│   └── .env              # Configuration
├── chatbot_api.py        # Updated with weather integration
├── models.py             # Database models
├── app.py                # Main Flask application
└── test_weather_agent.py # Test script
```

## Error Handling

The weather agent includes comprehensive error handling:
- Invalid city names
- Network connectivity issues
- API rate limits
- Missing API keys (falls back to mock data)

## Development

To extend the weather agent:

1. **Add new tools**: Create new functions in `weather_agent/agent.py`
2. **Update detection**: Modify `is_weather_query()` in `chatbot_api.py`
3. **Add new cities**: Update the city timezone mapping in `get_current_time()`

## Production Deployment

For production use:
1. Obtain real API keys for both Google AI Studio and OpenWeatherMap
2. Update the `.env` file with production keys
3. Consider implementing rate limiting
4. Add caching for frequently requested weather data

## Troubleshooting

### Common Issues

1. **"Weather information not available"**
   - Check if the city name is spelled correctly
   - Try major city names like "New York", "London", "Tokyo"

2. **"Error from Gemini"**
   - Verify your Google AI Studio API key is valid
   - Check your internet connection

3. **Mock data being returned**
   - This is normal if no OpenWeatherMap API key is configured
   - The agent will use realistic mock data for demonstration

For support, check the console logs for detailed error messages.
