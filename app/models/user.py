import bcrypt
from bson import ObjectId
from pymongo import MongoClient

# Connect to MongoDB Atlas (same as in app.py)
MONGO_URI = "mongodb+srv://tuyenboy1234:admin>@check-in-app.jtsl3.mongodb.net/web-chat?retryWrites=true&w=majority&appName=check-in-app"
client = MongoClient(MONGO_URI)
db = client.userdb
users_collection = db.users

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