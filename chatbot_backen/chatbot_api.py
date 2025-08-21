# chatbot_api/messages_bp.py
import os
from dotenv import load_dotenv
from flask import Blueprint, request, jsonify
from mongoengine import DoesNotExist
from models import ChatRoom, Message
from werkzeug.utils import secure_filename
import google.generativeai as genai  # Import the Gemini API library
import re
from weather_agent.agent import weather_agent, get_weather, get_current_time, get_weather_forecast

message_bp = Blueprint('messages', __name__, url_prefix='/messages')

load_dotenv()  # Load environment variables from .env

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable not set!")

genai.configure(api_key=GOOGLE_API_KEY)

# Configure safety settings for less restrictive filtering
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_ONLY_HIGH"
    }
]

# Use gemini-1.5-pro for better image processing
model = genai.GenerativeModel('gemini-2.5-pro')

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def is_weather_query(text):
    """Check if the text contains weather-related keywords."""
    weather_keywords = [
        'weather', 'temperature', 'forecast', 'rain', 'raining', 'sunny', 'cloudy', 'snow', 'snowing',
        'wind', 'windy', 'humidity', 'hot', 'cold', 'warm', 'cool', 'climate', 'storm',
        'what\'s the weather', 'how\'s the weather', 'weather report', 'weather in',
        'is it raining', 'is it snowing', 'is it sunny', 'is it cloudy', 'is it windy',
        'is it hot', 'is it cold', 'is it warm', 'is it cool'
    ]
    
    time_keywords = [
        'time', 'current time', 'what time', 'time in', 'clock', 'hour', 'minute'
    ]
    
    text_lower = text.lower()
    
    # Check for weather keywords
    for keyword in weather_keywords:
        if keyword in text_lower:
            return True, 'weather'
    
    # Check for time keywords
    for keyword in time_keywords:
        if keyword in text_lower:
            return True, 'time'
    
    return False, None


def extract_city_from_query(text):
    """Extract city name from weather/time query."""
    # Common patterns for city extraction - order matters!
    patterns = [
        # Specific time patterns first
        r'what\s+time\s+is\s+it\s+(?:in|at)\s+([a-zA-Z\s]+?)(?:\?|$|\.)',
        r'(?:current\s+time|time)\s+(?:in|at)\s+([a-zA-Z\s]+?)(?:\?|$|\.)',
        
        # Weather-specific patterns
        r'(?:what\'s|how\'s)\s+the\s+(?:weather|time)\s+(?:in|at)\s+([a-zA-Z\s]+?)(?:\?|$|\.)',
        r'(?:is\s+it|are\s+there)\s+(?:raining|snowing|sunny|cloudy|windy|hot|cold|warm|cool)\s+(?:in|at)\s+([a-zA-Z\s]+?)(?:\?|$|\.)',
        
        # General patterns last
        r'(?:weather|forecast|temperature)\s+(?:in|for|at)\s+([a-zA-Z\s]+?)(?:\?|$|\.)',
        r'(?:rain|snow|sun|wind|storm|temperature|hot|cold|warm|cool)\s+(?:in|at)\s+([a-zA-Z\s]+?)(?:\?|$|\.)',
        r'(?:in|at)\s+([a-zA-Z\s]+?)(?:\?|$|\.|,)\s*(?:is\s+it|what\'s|how\'s|weather|raining|snowing)',
        
        # Fallback patterns
        r'([a-zA-Z\s]+?)\s+(?:weather|time|forecast|temperature)',
    ]
    
    text_lower = text.lower()
    
    for pattern in patterns:
        match = re.search(pattern, text_lower)
        if match:
            city = match.group(1).strip()
            # Clean up common words that aren't city names
            exclude_words = ['the', 'a', 'an', 'today', 'tomorrow', 'now', 'current']
            city_words = [word for word in city.split() if word not in exclude_words]
            if city_words:
                return ' '.join(city_words)
    
    # Default fallback cities if no city is found
    return None


def handle_weather_query(text):
    """Handle weather-related queries using the weather agent tools."""
    is_weather, query_type = is_weather_query(text)
    
    if not is_weather:
        return None
    
    city = extract_city_from_query(text)
    if not city:
        return {
            "status": "error",
            "error_message": "Please specify a city for weather/time information. For example: 'What's the weather in New York?'"
        }
    
    text_lower = text.lower()
    
    # Handle forecast queries
    if 'forecast' in text_lower or 'tomorrow' in text_lower or 'next' in text_lower:
        days = 3  # Default forecast days
        if 'tomorrow' in text_lower:
            days = 1
        elif '5 day' in text_lower or 'five day' in text_lower:
            days = 5
        
        return get_weather_forecast(city, days)
    
    # Handle time queries
    elif query_type == 'time' or 'time' in text_lower:
        return get_current_time(city)
    
    # Handle weather queries
    else:
        return get_weather(city)


@message_bp.route('/messages/gemini', methods=['POST'])
def create_message():
    """Creates a new message (text or image) and interacts with Gemini."""
    print("Received a POST request to /messages")
    print(f"Form data: {dict(request.form)}")
    print(f"Files: {list(request.files.keys())}")

    try:
        chatroom_id = request.form.get('chatroom_id')
        sender = request.form.get('sender')

        if not all([sender, chatroom_id]):
            print(f"Missing fields - sender: {sender}, chatroom_id: {chatroom_id}")
            return jsonify({'error': 'Missing required fields (sender and chatroom_id)'}), 400

        try:
            chatroom = ChatRoom.objects.get(pk=chatroom_id)
        except ChatRoom.DoesNotExist:
            print(f"Chatroom not found: {chatroom_id}")
            return jsonify({'error': 'Chat room not found'}), 404

        # Check if a file was uploaded
        file_upload = request.files.get('file')  # Use .get to avoid KeyError
        text = request.form.get('text')
        
        print(f"File upload: {file_upload}")
        print(f"Text: {text}")

        if file_upload:
            print(f"File filename: {file_upload.filename}")
            if file_upload.filename == '':
                print("Empty filename detected")
                return jsonify({'error': 'No file selected'}), 400

            if file_upload and allowed_file(file_upload.filename):
                print(f"File allowed, processing...")
                filename = secure_filename(file_upload.filename)
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file_upload.save(filepath)
                print(f"File saved to: {filepath}")

                message = Message(sender=sender, chatRoom=chatroom, image_url=filepath)

                # --- Gemini Integration for Image ---
                try:
                    # Open the image file to create prompt
                    with open(filepath, 'rb') as f:
                        image_data = f.read()

                    # Formulate the gemini prompt
                    gemini_prompt_parts = [text if text else "Describe this image",
                                           {"mime_type": "image/jpeg", "data": image_data}]  # Ensure MIME Type is correct

                    # Generate the Gemini response with safety settings
                    response = model.generate_content(
                        gemini_prompt_parts,
                        safety_settings=safety_settings
                    )

                    # Check if the response was blocked by safety filters
                    if hasattr(response, 'candidates') and response.candidates:
                        candidate = response.candidates[0]
                        if hasattr(candidate, 'finish_reason'):
                            if candidate.finish_reason == 1:  # STOP
                                # Check if response has valid text content
                                try:
                                    if response.text:
                                        gemini_response = response.text
                                    else:
                                        gemini_response = "I couldn't generate a response for this image."
                                except ValueError:
                                    # This happens when response.text is accessed but no valid parts exist
                                    gemini_response = "I couldn't generate a response for this image."
                            elif candidate.finish_reason == 3:  # SAFETY
                                # Log safety filter details for debugging
                                safety_ratings = getattr(candidate, 'safety_ratings', [])
                                print(f"Safety filter triggered. Ratings: {[(rating.category, rating.probability) for rating in safety_ratings]}")
                                gemini_response = "I'm sorry, but I cannot process this image due to safety guidelines. Please try uploading a different image."
                            elif candidate.finish_reason == 4:  # RECITATION
                                gemini_response = "This image appears to contain copyrighted content. Please try a different image."
                            else:
                                print(f"Unexpected finish_reason: {candidate.finish_reason}")
                                gemini_response = "I wasn't able to generate a response for this image. Please try again."
                        else:
                            # No finish_reason, try to get text
                            try:
                                if response.text:
                                    gemini_response = response.text
                                else:
                                    gemini_response = "I wasn't able to generate a response for this image. Please try again."
                            except ValueError:
                                gemini_response = "I wasn't able to generate a response for this image. Please try again."
                    else:
                        print("No candidates in response")
                        gemini_response = "No response was generated for this image. Please try again."

                    #Store the response
                    message.gemini_response = gemini_response
                    message.save()

                except Exception as gemini_err:
                    print(f"Gemini API Error: {gemini_err}")
                    message.gemini_response = f"Error from Gemini: {gemini_err}"  # Store Error
                    message.save()

            else:
                print(f"Invalid file type for file: {file_upload.filename}")
                return jsonify({'error': 'Invalid file type'}), 400

        elif text:
            # Handle text-only messages
            message = Message(text=text, sender=sender, chatRoom=chatroom)

            # Check if this is a weather-related query first
            weather_response = handle_weather_query(text)
            
            if weather_response:
                if weather_response.get('status') == 'success':
                    gemini_response = weather_response['report']
                else:
                    gemini_response = weather_response.get('error_message', 'Sorry, I couldn\'t process your weather request.')
                
                message.gemini_response = gemini_response
                message.save()
            else:
                # --- Standard Gemini Integration for Text ---
                try:
                    response = model.generate_content(
                        text,
                        safety_settings=safety_settings
                    )  # Generate the response
                    
                    # Safely access response text
                    try:
                        gemini_response = response.text  # get the text
                    except ValueError:
                        # Handle case where response.text is not available
                        gemini_response = "I couldn't generate a response to your message. Please try again."
                    
                    message.gemini_response = gemini_response #Saves the gemini response to the DB
                    message.save()

                except Exception as gemini_err:
                    print(f"Gemini API Error: {gemini_err}")
                    message.gemini_response = f"Error from Gemini: {gemini_err}"  # Store Error
                    message.save()
        else:
            return jsonify({'error': 'Missing text or file'}), 400  # Neither text nor file

        # Create the AI Message object

        ai_message = Message(
            text=message.gemini_response,
            sender='ai',
            chatRoom=chatroom
        )

        ai_message.save()

        chatroom.message_count += 1
        chatroom.save()

        return jsonify(ai_message.to_json()), 201

    except Exception as e:
        print(f"Error creating message: {e}")
        return jsonify({'error': str(e)}), 500


@message_bp.route('/weather', methods=['POST'])
def get_weather_info():
    """Direct endpoint for weather agent queries."""
    try:
        data = request.get_json()
        query = data.get('query', '')
        chatroom_id = data.get('chatroom_id')
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        if not chatroom_id:
            return jsonify({'error': 'Chatroom ID is required'}), 400
        
        try:
            chatroom = ChatRoom.objects.get(pk=chatroom_id)
        except ChatRoom.DoesNotExist:
            return jsonify({'error': 'Chat room not found'}), 404
        
        # Save user message
        user_message = Message(text=query, sender='user', chatRoom=chatroom)
        user_message.save()
        
        # Handle the weather query
        weather_response = handle_weather_query(query)
        
        if weather_response:
            if weather_response.get('status') == 'success':
                response_text = weather_response['report']
            else:
                response_text = weather_response.get('error_message', 'Sorry, I couldn\'t process your weather request.')
        else:
            response_text = "I can help you with weather information, current time, and forecasts. Please ask about the weather or time in a specific city."
        
        # Save AI response
        ai_message = Message(
            text=response_text,
            sender='ai',
            chatRoom=chatroom,
            gemini_response=response_text
        )
        ai_message.save()
        
        chatroom.message_count += 2  # User message + AI response
        chatroom.save()
        
        return jsonify({
            'user_message': user_message.to_json(),
            'ai_response': ai_message.to_json()
        }), 201
        
    except Exception as e:
        print(f"Error handling weather query: {e}")
        return jsonify({'error': str(e)}), 500


@message_bp.route('/weather/capabilities', methods=['GET'])
def get_weather_capabilities():
    """Get information about weather agent capabilities."""
    capabilities = {
        "supported_functions": [
            {
                "name": "get_weather",
                "description": "Get current weather for a city",
                "example": "What's the weather in New York?"
            },
            {
                "name": "get_current_time", 
                "description": "Get current time for a city",
                "example": "What time is it in Tokyo?"
            },
            {
                "name": "get_weather_forecast",
                "description": "Get weather forecast for 1-5 days",
                "example": "What's the forecast for London?"
            }
        ],
        "supported_cities": [
            "New York", "London", "Paris", "Tokyo", "Los Angeles", "Chicago",
            "Sydney", "Moscow", "Beijing", "Mumbai", "Dubai", "Singapore",
            "Berlin", "Rome", "Madrid", "Toronto", "Vancouver", "Mexico City",
            "São Paulo", "Buenos Aires", "and many more..."
        ],
        "example_queries": [
            "What's the weather in Paris?",
            "Current time in Tokyo",
            "5-day forecast for London",
            "Is it raining in New York?",
            "Temperature in Sydney"
        ]
    }
    
    return jsonify(capabilities)