# app_pythonanywhere.py - Production version for PythonAnywhere
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from models_mysql import db, ChatRoom, Message
from chatbot_api import message_bp
import logging
import git

# Configure logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Production CORS configuration
CORS(app, origins=[
    "https://mandyy1223.pythonanywhere.com",  # Your main domain
    "https://mandyy1223.eu.pythonanywhere.com",  # Alternative domain format
    "http://localhost:3000",   # For local development
    "http://localhost:5173",   # For Vite dev server
    "http://localhost:5174"    # For Vite dev server (alternate port)
])

# MySQL Database configuration for PythonAnywhere
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{os.environ.get('DB_USER')}:"
    f"{os.environ.get('DB_PASSWORD')}@"
    f"{os.environ.get('DB_HOST')}/"
    f"{os.environ.get('DB_NAME')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Register the chatbot Blueprint
app.register_blueprint(message_bp, url_prefix='/api')

@app.route('/update_server', methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('path/to/git_repo')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400

@app.route('/api/chatRooms', methods=['GET'])
def get_chatRooms():
    """Retrieves a list of all chat rooms."""
    try:
        chat_rooms = ChatRoom.query.all()
        chat_room_list = [room.to_json() for room in chat_rooms]
        return jsonify(chat_room_list)
    except Exception as e:
        app.logger.error(f"Error retrieving chat rooms: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/chatRooms', methods=['POST'])
def create_chatroom():
    """Creates a new chat room."""
    try:
        data = request.get_json()
        name = data.get('name')

        if not name:
            return jsonify({'error': 'Chat room name is required'}), 400

        # Check if a chat room with the same name already exists
        existing_chatroom = ChatRoom.query.filter_by(name=name).first()
        if existing_chatroom:
            return jsonify({'error': 'Chat room with this name already exists'}), 409

        chatroom = ChatRoom(name=name)
        db.session.add(chatroom)
        db.session.commit()

        return jsonify({
            'message': 'Chat room created successfully', 
            'id': str(chatroom.id), 
            'name': name
        }), 201

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error creating chat room: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/chatRooms', methods=['DELETE'])
def delete_all_chatrooms():
    """Deletes all chat rooms from the database."""
    try:
        ChatRoom.query.delete()
        db.session.commit()
        return jsonify({'message': 'All chat rooms deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error deleting chat rooms: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/chatRooms/<int:chatroom_id>', methods=['DELETE'])
def delete_chatroom(chatroom_id):
    """Deletes a chatroom and its associated messages."""
    try:
        chatroom = ChatRoom.query.get_or_404(chatroom_id)
        db.session.delete(chatroom)
        db.session.commit()
        return jsonify({'message': 'Chatroom and associated messages deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error deleting chatroom: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/chatRooms/<int:chatroom_id>/messages', methods=['GET'])
def get_messages(chatroom_id):
    """Retrieves messages for a specific chat room, ordered by timestamp."""
    try:
        chatroom = ChatRoom.query.get_or_404(chatroom_id)
        messages = Message.query.filter_by(chatRoom_id=chatroom_id).order_by(Message.timestamp).all()
        message_list = [message.to_json() for message in messages]
        return jsonify(message_list), 200
    except Exception as e:
        app.logger.error(f"Error retrieving messages: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/messages', methods=['POST'])
def create_message():
    """Creates a new message and associates it with a chat room."""
    try:
        data = request.get_json()
        text = data.get('text')
        sender = data.get('sender')
        chatroom_id = data.get('chatroom_id')

        if not all([text, sender, chatroom_id]):
            return jsonify({'error': 'Missing required fields'}), 400

        chatroom = ChatRoom.query.get_or_404(chatroom_id)
        message = Message(text=text, sender=sender, chatRoom_id=chatroom.id)
        
        db.session.add(message)
        chatroom.message_count += 1
        db.session.commit()

        return jsonify({
            'message': 'Message created successfully', 
            'id': str(message.id)
        }), 201

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error creating message: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/messages/<int:message_id>', methods=['PUT'])
def edit_message(message_id):
    """Edits an existing message."""
    try:
        data = request.get_json()
        new_text = data.get('text')

        if not new_text:
            return jsonify({'error': 'Text is required'}), 400

        message = Message.query.get_or_404(message_id)

        # Only allow editing user messages, not bot responses
        if message.sender != 'user':
            return jsonify({'error': 'Only user messages can be edited'}), 403

        message.text = new_text
        db.session.commit()

        return jsonify({
            'message': 'Message updated successfully', 
            'data': message.to_json()
        }), 200

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error editing message: {e}")
        return jsonify({'error': str(e)}), 500

# Create tables
@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=False)  # Set to False for production
