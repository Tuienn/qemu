from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
import bcrypt
import os
from bson import ObjectId

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.secret_key = 'your_secret_key'  # In production, use a proper secret key

# Connect to MongoDB Atlas
MONGO_URI = "mongodb+srv://username:password@cluster.mongodb.net/userdb?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client.userdb
users_collection = db.users

# Import routes
from app.routes import auth_routes

# Register blueprints
app.register_blueprint(auth_routes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True) 