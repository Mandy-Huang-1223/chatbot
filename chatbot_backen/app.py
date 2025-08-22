# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from mongoengine import connect
from models import ChatRoom, Message
from chatbot_api import message_bp  # Import the chatbot Blueprint
import git  

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure MongoDB connection (replace with your details)
connect('chatbot', host='mongodb://localhost:27017/')  # <--- Changed this line

# Register the chatbot Blueprint
app.register_blueprint(message_bp, url_prefix='/api')  # Mount the chatbot API under /api


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
        chat_rooms = ChatRoom.objects.all()
        chat_room_list = [room.to_json() for room in chat_rooms]
        return jsonify(chat_room_list)
    except Exception as e:
        print(f"Error retrieving chat rooms: {e}")
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
         existing_chatroom = ChatRoom.objects(name=name).first()
         if existing_chatroom:
             return jsonify({'error': 'Chat room with this name already exists'}), 409

         chatroom = ChatRoom(name=name)  # ONLY set the name!
         chatroom.save()

         # Include the id in the response after creating
         return jsonify({'message': 'Chat room created successfully', 'id': str(chatroom.pk), 'name': name}), 201

     except Exception as e:
         print(f"Error creating chat room: {e}")
         return jsonify({'error': str(e)}), 500
    
@app.route('/api/chatRooms', methods=['DELETE'])
def delete_all_chatRooms():
    """Deletes all chat rooms from the database."""
    try:
        ChatRoom.objects.delete()  # Delete all chat rooms
        return jsonify({'message': 'All chat rooms deleted successfully'}), 200
    except Exception as e:
        print(f"Error deleting chat rooms: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/chatRooms/<chatroom_id>', methods=['DELETE'])
def delete_chatroom(chatroom_id):
    """Deletes a chatroom and its associated messages."""
    try:
        chatroom = ChatRoom.objects.get(pk=chatroom_id)

        # Delete all messages associated with the chatroom
        Message.objects(chatRoom=chatroom).delete()

        # Delete the chatroom itself
        chatroom.delete()

        return jsonify({'message': 'Chatroom and associated messages deleted successfully'}), 200

    except Exception as e:
        print(f"Error deleting chatroom: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/chatRooms/<chatroom_id>/messages', methods=['GET'])
def get_messages(chatroom_id):
    """Retrieves messages for a specific chat room, ordered by timestamp."""
    try:
        try:
            chatroom = ChatRoom.objects.get(pk=chatroom_id)
        except ChatRoom.DoesNotExist:
            return jsonify({'error': 'Chat room not found'}), 404

        messages = Message.objects(chatRoom=chatroom).order_by('timestamp') # Retrieve and order the messages
        message_list = [message.to_json() for message in messages]  # Convert to JSON

        return jsonify(message_list), 200

    except Exception as e:
        print(f"Error retrieving messages: {e}")
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/messages', methods=['POST'])
def create_message():
    print("Received a POST request to /api/messages")
    """Creates a new message and associates it with a chat room."""
    try:
        data = request.get_json()
        text = data.get('text')
        sender = data.get('sender')
        chatroom_id = data.get('chatroom_id')

        if not all([text, sender, chatroom_id]):
            return jsonify({'error': 'Missing required fields'}), 400

        try:
            chatroom = ChatRoom.objects.get(pk=chatroom_id)
        except ChatRoom.DoesNotExist:
            return jsonify({'error': 'Chat room not found'}), 404

        message = Message(text=text, sender=sender, chatRoom=chatroom)
        message.save()

        # OPTIONAL: If you keep the messages ListField in ChatRoom, update it:
        # chatroom.messages.append(message.id)
        chatroom.message_count += 1
        chatroom.save()

        return jsonify({'message': 'Message created successfully', 'id': str(message.pk)}), 201

    except Exception as e:
        print(f"Error creating message: {e}")
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/messages/<message_id>', methods=['PUT'])
def edit_message(message_id):
    """Edits an existing message."""
    try:
        data = request.get_json()
        new_text = data.get('text')

        if not new_text:
            return jsonify({'error': 'Text is re uired'}), 400

        try:
            message = Message.objects.get(pk=message_id)
        except Message.DoesNotExist:
            return jsonify({'error': 'Message not found'}), 404

        # Only allow editing user messages, not bot responses
        if message.sender != 'user':
            return jsonify({'error': 'Only user messages can be edited'}), 403

        message.text = new_text
        message.save()

        return jsonify({'message': 'Message updated successfully', 'data': message.to_json()}), 200

    except Exception as e:
        print(f"Error editing message: {e}")
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)
