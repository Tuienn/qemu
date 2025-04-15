from pymongo import MongoClient
import os
from dotenv import load_dotenv
import bcrypt

# Load environment variables
load_dotenv()

# Connect to MongoDB Atlas using environment variable
MONGO_URI = os.getenv('MONGO_URI')
if not MONGO_URI:
    raise ValueError("MONGO_URI environment variable not set. Please check your .env file.")

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
    # Create dummy collections to prevent errors
    class DummyCollection:
        def find_one(self, *args, **kwargs): return None
        def find(self, *args, **kwargs): return []
        def insert_one(self, *args, **kwargs): return None
    
    users_collection = DummyCollection()
    messages_collection = DummyCollection()
