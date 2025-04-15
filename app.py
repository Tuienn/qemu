from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
import bcrypt
import os
from bson import ObjectId

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
    print("Successfully connected to MongoDB Atlas!")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
    # Continuing without database will likely cause errors later

# Import routes
from app.routes import auth_routes

# Register blueprints
app.register_blueprint(auth_routes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True) 