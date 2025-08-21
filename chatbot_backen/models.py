# models.py
from mongoengine import Document, StringField, ListField, IntField, ReferenceField, DateTimeField
import uuid
import datetime  # Import the datetime module


class ChatRoom(Document):
    name = StringField(required=True, unique=True)  # Chat room name
    message_count = IntField(default=0)  # Message count

    def to_json(self):
        return {
            "id": str(self.pk),  # Convert ObjectId to string
            "name": self.name,
            "message_count": self.message_count,
        }


class Message(Document):
    text = StringField()
    sender = StringField(choices=['user', 'ai'])
    chatRoom = ReferenceField(ChatRoom)
    timestamp = DateTimeField(default=datetime.datetime.now)  # Add a timestamp
    gemini_response = StringField() #Store Gemini's Response
    image_url = StringField() # Stores the image url or path

    def to_json(self):
        return {
            "id": str(self.pk),
            "text": self.text,
            "sender": self.sender,
            "chatRoom": str(self.chatRoom.pk) if self.chatRoom else None,  # Handle potential None value
            "timestamp": self.timestamp.isoformat(),  # Include timestamp
            # "gemini_response": self.gemini_response if self.gemini_response else None,  # Include Gemini response
            "image": self.image_url if self.image_url else None
        }