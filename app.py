from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
import bcrypt
import os
from bson import ObjectId
import json
from datetime import datetime

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.secret_key = '123456'  # In production, use a proper secret key

# Connect to MongoDB Atlas
MONGO_URI = "mongodb+srv://tuyenboy1234:admin@check-in-app.jtsl3.mongodb.net/web-chat?retryWrites=true&w=majority&appName=check-in-app"
try:
    client = MongoClient(MONGO_URI)
    # Test connection
    client.admin.command('ping')
    db = client.userdb
    users_collection = db.users
    messages_collection = db.messages
    print("Successfully connected to MongoDB Atlas!")
    
    # Debug: Log all users in database
    print("\n==== USERS IN DATABASE ====")
    users = list(users_collection.find())
    for user in users:
        # Convert ObjectId to string for printing
        user['_id'] = str(user['_id'])
        # Convert binary password to string representation for printing
        if isinstance(user['password'], bytes):
            user['password'] = str(user['password'])
        print(f"User: {user}")
    print(f"Total users: {len(users)}")
    print("==========================\n")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
    # Continuing without database will likely cause errors later

# Import routes
from app.routes import auth_routes

# Register blueprints
app.register_blueprint(auth_routes)

# Add debug middleware for authentication
@app.before_request
def debug_auth():
    if request.endpoint == 'auth.login' and request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(f"\n==== LOGIN ATTEMPT ====")
        print(f"Username: {username}")
        print(f"Password: {'*' * len(password) if password else 'None'}")
        
        # Find user document
        user_doc = users_collection.find_one({"username": username})
        print(f"User found in database: {user_doc is not None}")
        
        if user_doc:
            # For debugging - don't show full password in logs
            print(f"User from DB: {str(user_doc['_id'])}, Username: {user_doc['username']}")
            
            # Check if password matches
            password_matches = False
            try:
                password_matches = bcrypt.checkpw(password.encode('utf-8'), user_doc["password"])
            except Exception as e:
                print(f"Password check error: {e}")
                
            print(f"Password matches: {password_matches}")
        print("=======================\n")

class ChatMessage:
    def __init__(self, user_id, username, content, timestamp=None, message_id=None):
        self.id = message_id
        self.user_id = user_id
        self.username = username
        self.content = content
        self.timestamp = timestamp or datetime.now()
        
    @staticmethod
    def create_message(user_id, username, content):
        # Create message document
        message_data = {
            "user_id": user_id,
            "username": username,
            "content": content,
            "timestamp": datetime.now()
        }
        
        # Insert message into database
        result = messages_collection.insert_one(message_data)
        
        if result.inserted_id:
            return ChatMessage(
                user_id, 
                username, 
                content, 
                message_data["timestamp"],
                str(result.inserted_id)
            )
        return None
    
    @staticmethod
    def get_all_messages(limit=50):
        # Get the most recent messages
        cursor = messages_collection.find().sort("timestamp", -1).limit(limit)
        messages = []
        
        for msg in cursor:
            messages.append(ChatMessage(
                msg["user_id"],
                msg["username"],
                msg["content"],
                msg["timestamp"],
                str(msg["_id"])
            ))
        
        # Return in chronological order (oldest first)
        return list(reversed(messages))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True) 