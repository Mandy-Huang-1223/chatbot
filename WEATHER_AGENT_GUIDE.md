# Weather Agent Integration - Complete Setup Guide

This guide shows you how to use the newly integrated Weather Agent in your chatbot project.

## What's New

Your chatbot now includes a Weather Agent powered by Google's Agent Development Kit (ADK) that can:

1. **Get Current Weather** - Real-time weather for any city
2. **Get Current Time** - Current time in different cities worldwide
3. **Get Weather Forecasts** - 1-5 day weather forecasts
4. **Automatic Detection** - The regular chat automatically detects and handles weather queries

## 🌟 Key Feature: Seamless Integration

**No special interface needed!** Simply chat naturally and ask weather questions alongside regular conversation. The system automatically detects weather queries and provides intelligent responses.

## How to Start the Application

### Backend (Flask)

1. **Navigate to backend directory:**
   ```bash
   cd chatbot_backen
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API keys (optional but recommended):**
   
   Edit `weather_agent/.env`:
   ```
   GOOGLE_API_KEY=your_google_ai_studio_key_here
   OPENWEATHER_API_KEY=your_openweather_key_here
   ```
   
   - Get Google AI Studio key: https://aistudio.google.com/apikey
   - Get OpenWeatherMap key: https://openweathermap.org/api (free)

4. **Start the Flask server:**
   ```bash
   python app.py
   ```

### Frontend (React)

1. **Navigate to frontend directory:**
   ```bash
   cd chat-bot-react
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

## Using the Weather Agent

Simply type weather-related questions directly in the regular chat interface:

**Example Queries:**
- "What's the weather in New York?"
- "Current time in Tokyo"
- "Is it raining in London?"
- "5-day forecast for Paris"
- "Temperature in Sydney"

The system automatically detects these queries and uses the Weather Agent instead of regular Gemini AI. No special interface or tab switching is needed - just chat naturally!

## API Endpoints

### Regular Message Endpoint (Now with Weather Detection)
**POST** `/api/messages/gemini`

Automatically detects weather queries and routes them to the Weather Agent.

### Weather Capabilities (Optional)
**GET** `/api/messages/weather/capabilities`

Returns information about supported functions and cities for development/debugging purposes.

## Supported Cities

The Weather Agent supports major cities worldwide including:

**Americas:** New York, Los Angeles, Chicago, Toronto, Vancouver, Mexico City, São Paulo, Buenos Aires

**Europe:** London, Paris, Berlin, Rome, Madrid, Moscow

**Asia-Pacific:** Tokyo, Beijing, Mumbai, Singapore, Dubai, Sydney

**And many more...**

## Features

### Smart Detection
The system intelligently detects weather-related queries using keywords like:
- weather, temperature, forecast, rain, sunny, cloudy
- time, current time, what time, clock
- Specific patterns like "weather in [city]"

### Fallback Support
- If no OpenWeatherMap API key is provided, uses realistic mock data
- If a city isn't supported, provides helpful error messages
- Network errors are handled gracefully

### Integration Benefits
- All weather conversations are saved in your MongoDB database
- Weather responses appear as regular chat messages
- Seamless, natural chat experience with automatic weather detection
- No need to switch interfaces or learn new commands

## Testing

Test the weather agent functionality:

```bash
cd chatbot_backen
python test_weather_agent.py
```

## Example Conversations

**User:** "What's the weather like in New York?"
**AI:** "The weather in New York is Sunny with a temperature of 25°C (77°F). Light wind from the southwest."

**User:** "What time is it in Tokyo?"
**AI:** "The current time in Tokyo is 2025-08-15 19:09:45 JST+0900"

**User:** "Give me the 3-day forecast for London"
**AI:** "Weather forecast for London:
Tomorrow: Overcast, 17°C (63°F)
Day 2: Light rain, 15°C (59°F)
Day 3: Partly cloudy, 19°C (66°F)"

**User:** "Thanks! Now tell me a joke"
**AI:** "Why don't scientists trust atoms? Because they make up everything!"

*Notice how you can seamlessly switch between weather queries and regular chat!*

## Troubleshooting

### Common Issues

1. **"Weather information not available"**
   - Check city name spelling
   - Try major cities like "New York", "London", "Tokyo"

2. **Import errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version (3.9+ required)

3. **React compilation errors**
   - Make sure all frontend dependencies are installed
   - The chatbot should work with standard React and Material-UI components

4. **Database connection issues**
   - Make sure MongoDB is running
   - Check connection string in `app.py`

### API Key Setup (Optional)

Without API keys, the system works with mock data. For production:

1. **Google AI Studio Key** (for ADK):
   - Required for the full ADK experience
   - Get from: https://aistudio.google.com/apikey

2. **OpenWeatherMap Key** (for real weather):
   - Optional - system uses mock data without it
   - Get free key from: https://openweathermap.org/api

## Architecture Overview

```
Project Structure:
├── chatbot_backen/
│   ├── weather_agent/          # Weather Agent implementation
│   │   ├── agent.py           # Core weather functions
│   │   ├── __init__.py
│   │   └── .env               # Configuration
│   ├── chatbot_api.py         # Enhanced with weather detection
│   ├── app.py                 # Main Flask app
│   ├── models.py              # Database models
│   └── requirements.txt       # Python dependencies
└── chat-bot-react/
    └── src/App.tsx            # Regular chat with weather integration
```

## Next Steps

1. **Get Real API Keys** for production use
2. **Customize Weather Functions** - Add more cities or weather features
3. **Extend the Agent** - Add more tools like maps, traffic, etc.
4. **Deploy** - Use the deployment guides in the ADK documentation

Enjoy your new Weather Agent! 🌤️
