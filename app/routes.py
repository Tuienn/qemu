from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import bcrypt
import sys
import os
from datetime import datetime
from bson import ObjectId

# Get the absolute path to the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add to Python path if not already present
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import the app itself to access its variables
import app as main_app

# Create a blueprint for routes
routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
    if 'user_id' in session:
        # Redirect to chat page if user is logged in
        return redirect(url_for('routes.chat'))
    # If not logged in, redirect to login page
    return redirect(url_for('routes.login'))

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username and password:
            user = main_app.users_collection.find_one({"username": username})
            
            if user and bcrypt.checkpw(password.encode('utf-8'), user["password"]):
                # Store user info in session
                session['user_id'] = str(user['_id'])
                session['username'] = user['username']
                
                # Redirect to chat page after successful login
                return redirect(url_for('routes.chat'))
            else:
                flash('Invalid username or password', 'error')
        else:
            flash('Please enter both username and password')
    
    return render_template('login.html')

@routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        name = request.form.get('name')
        
        # Check if username already exists
        if main_app.users_collection.find_one({"username": username}):
            flash('Username already exists', 'error')
            return redirect(url_for('routes.register'))
        
        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Create new user
        user_data = {
            "username": username,
            "password": hashed_password
        }
        
        # Add name if provided
        if name:
            user_data["name"] = name
            
        # Insert user into database
        user_id = main_app.users_collection.insert_one(user_data).inserted_id
        
        # Log the user in
        session['user_id'] = str(user_id)
        session['username'] = username
        
        # Redirect to chat page after registration
        return redirect(url_for('routes.chat'))
    
    return render_template('register.html')

@routes.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('routes.login'))

# Chat routes
@routes.route('/chat')
def chat():
    if 'user_id' not in session:
        flash('Please login to access the chat', 'error')
        return redirect(url_for('routes.login'))
    
    # Get recent messages
    messages = get_all_messages(50)
    
    return render_template('chat.html', 
                          user_id=session['user_id'], 
                          username=session['username'],
                          messages=messages)

@routes.route('/send_message', methods=['POST'])
def send_message():
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))
    
    content = request.form.get('message')
    if content and content.strip():
        create_message(
            session['user_id'],
            session['username'],
            content
        )
    
    return redirect(url_for('routes.chat'))

# Chat message functions
def create_message(user_id, username, content):
    """Create a new chat message in the database"""
    message_data = {
        "user_id": user_id,
        "username": username,
        "content": content,
        "timestamp": datetime.now()
    }
    
    # Insert message into database
    return main_app.messages_collection.insert_one(message_data)

def get_all_messages(limit=50):
    """Get the most recent messages from the database"""
    cursor = main_app.messages_collection.find().sort("timestamp", -1).limit(limit)
    messages = []
    
    for msg in cursor:
        messages.append({
            "id": str(msg["_id"]),
            "user_id": msg["user_id"],
            "username": msg["username"],
            "content": msg["content"],
            "timestamp": msg["timestamp"]
        })
    
    # Return in chronological order (oldest first)
    return list(reversed(messages))