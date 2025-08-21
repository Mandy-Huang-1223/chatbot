
# Gemini Chatbot – Multi-Modal Chat & Chatroom App

This app lets you chat with a Gemini-powered AI assistant using both text and images, and manage multiple chatrooms. You can send messages, upload images, create or delete chatrooms, and ask for real-time weather and time information for cities worldwide.

## ✨ Features

- **Chat with Gemini AI**: Send text or images and get intelligent responses from the Gemini robot.
- **Image Upload**: Send images to Gemini for analysis and conversation.
- **Multiple Chatrooms**: Create, switch, and delete chatrooms for different topics or groups.
- **Weather & Time Queries**: Ask about the weather or current time in any major city, powered by the integrated Weather Agent.


## 🚀 Getting Started

### 1. Backend (Flask)

1. Open a terminal and navigate to the backend folder:
   ```bash
   cd chatbot_backen
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. *(Optional, for real weather data)* Set up API keys:
   - Edit `weather_agent/.env` and add:
     ```
     GOOGLE_API_KEY=your_google_ai_studio_key_here
     OPENWEATHER_API_KEY=your_openweather_key_here
     ```
   - Get Google AI Studio key: https://aistudio.google.com/apikey
   - Get OpenWeatherMap key: https://openweathermap.org/api
4. Start the backend server:
   ```bash
   python app.py
   ```

### 2. Frontend (React)

1. Open a new terminal and navigate to the frontend folder:
   ```bash
   cd chat-bot-react
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the frontend development server:
   ```bash
   npm run dev
   ```

The app will be available at the URL shown in your terminal (usually http://localhost:5173).


## 🧑‍💻 How to Use

### Chatting with Gemini
- Type a message in the chat input and press Enter to send.
- To send an image, use the image upload button (paperclip or image icon), select an image, and send it. Gemini will analyze and respond to both text and images.

### Managing Chatrooms
- **Create a chatroom:** Click the “+” or “New Chatroom” button, enter a name, and confirm.
- **Switch chatrooms:** Click on a chatroom tab to switch.
- **Delete a chatroom:** Click the delete/trash icon on a chatroom tab and confirm.

### Weather & Time Queries
- Ask questions like:
   - "What's the weather in New York?"
   - "Current time in Tokyo"
   - "5-day forecast for Paris"
- The app will automatically detect and answer weather/time questions using the Weather Agent.


## 🌍 Supported Cities for Weather
The Weather Agent supports most major cities worldwide (e.g., New York, London, Tokyo, Paris, Sydney, and more).


## 🛠️ Troubleshooting

**Backend issues:**
- Make sure all Python dependencies are installed: `pip install -r requirements.txt`
- Python 3.9+ is required
- If using real weather, check your API keys in `weather_agent/.env`

**Frontend issues:**
- Make sure all dependencies are installed: `npm install`
- If you see errors, try restarting the dev server

**Database issues:**
- Ensure MongoDB is running and the connection string in `app.py` is correct

**Weather not working?**
- Without API keys, mock data is used
- Try major cities if a city is not found


## 📝 Example Conversations

**Text & Image Chat:**
> User: "Show me a cat picture!" *(uploads image)*
> Gemini: "That's a cute cat! Did you know cats sleep up to 16 hours a day?"

**Weather Query:**
> User: "What's the weather in New York?"
> Gemini: "The weather in New York is sunny with a temperature of 25°C."

**Chatroom Management:**
> User creates a new chatroom "Work" and switches between "Work" and "Friends" chatrooms.

**Seamless Experience:**
> User: "Tell me a joke"
> Gemini: "Why don't scientists trust atoms? Because they make up everything!"


## 🏗️ Architecture Overview

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
   └── src/App.tsx            # Main React app (chat, image, chatrooms)
```


---

Enjoy chatting with Gemini, sharing images, and managing your own chatrooms!
