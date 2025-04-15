from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import bcrypt
from app.app import users_collection, messages_collection
from datetime import datetime
from bson import ObjectId

# Create a blueprint for authentication routes
auth_routes = Blueprint('auth', __name__)

@auth_routes.route('/')
def index():
    if 'user_id' in session:
        # Redirect to chat page if user is logged in
        return redirect(url_for('auth.chat'))
    # If not logged in, redirect to login page
    return redirect(url_for('auth.login'))

@auth_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username and password:
            user = users_collection.find_one({"username": username})
            
            if user and bcrypt.checkpw(password.encode('utf-8'), user["password"]):
                # Store user info in session
                session['user_id'] = str(user['_id'])
                session['username'] = user['username']
                
                # Redirect to chat page after successful login
                return redirect(url_for('auth.chat'))
            else:
                flash('Invalid username or password', 'error')
        else:
            flash('Please enter both username and password')
    
    return render_template('login.html')

@auth_routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        name = request.form.get('name')
        
        # Check if username already exists
        if users_collection.find_one({"username": username}):
            flash('Username already exists', 'error')
            return redirect(url_for('auth.register'))
        
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
        user_id = users_collection.insert_one(user_data).inserted_id
        
        # Log the user in
        session['user_id'] = str(user_id)
        session['username'] = username
        
        # Redirect to chat page after registration
        return redirect(url_for('auth.chat'))
    
    return render_template('register.html')

@auth_routes.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

# Chat routes
@auth_routes.route('/chat')
def chat():
    if 'user_id' not in session:
        flash('Please login to access the chat', 'error')
        return redirect(url_for('auth.login'))
    
    # Get recent messages
    messages = get_all_messages(50)
    
    return render_template('chat.html', 
                          user_id=session['user_id'], 
                          username=session['username'],
                          messages=messages)

@auth_routes.route('/send_message', methods=['POST'])
def send_message():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    content = request.form.get('message')
    if content and content.strip():
        create_message(
            session['user_id'],
            session['username'],
            content
        )
    
    return redirect(url_for('auth.chat'))

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
    return messages_collection.insert_one(message_data)

def get_all_messages(limit=50):
    """Get the most recent messages from the database"""
    cursor = messages_collection.find().sort("timestamp", -1).limit(limit)
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