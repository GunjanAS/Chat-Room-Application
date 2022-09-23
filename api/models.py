"""Application Models"""
import bson
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
load_dotenv()
DATABASE_URL = os.environ.get(
    'DATABASE_URL') or 'mongodb://localhost:27017/sampleDB'
print(DATABASE_URL)
client = MongoClient(DATABASE_URL)
db = client.SampleDB


class ChatLog:
    """Chat log Model"""

    def __init__(self):
        return

    def create(self, text="", type="chat", timestamp="", user_email=""):
        """Create a new chat"""
        new_chat = db.chatlog.insert_one(
            {
                "text": text,
                "type": type,
                "timestamp": timestamp,
                "user_email": user_email
            }
        )
        return True

    def get_all_sorterd(self, limit=500, sort='_id', direction=1):
        """Get all chats in desc order of timestamp [_id]"""
        chats = db.chatlog.find().limit(limit).sort(sort, direction)
        return [{**chat, "_id": str(chat["_id"])} for chat in chats]

    def get_by_type(self, type="chat", limit=500, sort='_id', direction=1):
        """Get all chats by type [event | chat]"""
        chats = db.chatlog.find({"type": type}).limit(
            limit).sort(sort, direction)
        return [{**chat, "_id": str(chat["_id"])} for chat in chats]


class User:
    """User Model"""

    def __init__(self):
        return

    def create(self, name="", email="", password=""):
        """Create a new user"""
        user = self.get_by_email(email)
        if user:
            return False
        new_user = db.users.insert_one(
            {
                "name": name,
                "email": email,
                "password": generate_password_hash(password),
                "active": True
            }
        )
        return self.get_by_id(new_user.inserted_id)

    def get_all(self):
        """Get all users"""
        users = db.users.find({"active": True})
        return [{**user, "_id": str(user["_id"])} for user in users]

    def get_by_id(self, user_id):
        """Get a user by id"""
        user = db.users.find_one(
            {"_id": bson.ObjectId(user_id), "active": True})
        if not user:
            return
        print("got user", user)
        user["_id"] = str(user["_id"])
        user.pop("password")
        return user

    def get_by_email(self, email):
        """Get a user by email"""
        user = db.users.find_one({"email": email, "active": True})
        if not user:
            return
        user["_id"] = str(user["_id"])
        return user

    def disable(self, user_id):
        """Disable a user account"""
        user = db.users.update_one(
            {"_id": bson.ObjectId(user_id)},
            {"$set": {"active": False}}
        )
        user = self.get_by_id(user_id)
        return user

    def login(self, email, password):
        """Login a user"""
        user = self.get_by_email(email)
        if not user or not check_password_hash(user["password"], password):
            return
        user.pop("password")
        return user
