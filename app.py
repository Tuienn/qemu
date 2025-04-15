from flask import Flask, render_template, request, redirect, url_for, session, flash
import bcrypt
import os
from bson import ObjectId
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import database connections
from database import users_collection, messages_collection

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.secret_key = os.getenv('SECRET_KEY', '123456')  # Use environment variable if available

# Register blueprints
from app.routes import routes
app.register_blueprint(routes)

# Add debug middleware for authentication
@app.before_request
def debug_auth():
    if request.endpoint == 'routes.login' and request.method == 'POST':
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)