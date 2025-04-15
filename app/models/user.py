import bcrypt
from bson import ObjectId
import os
import sys

# Get the absolute path to the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
# Add to Python path if not already present
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import the database connection from the central module
from database import users_collection

class User:
    def __init__(self, username, password, name, user_id=None):
        self.id = user_id
        self.username = username
        self.password = password
        self.name = name
        
    @staticmethod
    def create_user(username, password, name):
        # Check if username already exists
        if users_collection.find_one({"username": username}):
            return None
            
        # Hash the password
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Create user document
        user_data = {
            "username": username,
            "password": hashed_pw,
            "name": name
        }
        
        # Insert user into database
        result = users_collection.insert_one(user_data)
        
        if result.inserted_id:
            return User(username, hashed_pw, name, str(result.inserted_id))
        return None
    
    @staticmethod
    def authenticate(username, password):
        # Find user by username
        user_data = users_collection.find_one({"username": username})
        
        if user_data and bcrypt.checkpw(password.encode('utf-8'), user_data["password"]):
            return User(
                user_data["username"], 
                user_data["password"], 
                user_data["name"], 
                str(user_data["_id"])
            )
        return None
        
    @staticmethod
    def get_by_id(user_id):
        user_data = users_collection.find_one({"_id": ObjectId(user_id)})
        if user_data:
            return User(
                user_data["username"], 
                user_data["password"], 
                user_data["name"], 
                str(user_data["_id"])
            )
        return None