from models import ChatLog, User
from schemas import validate_user
import os
from dotenv import load_dotenv
import datetime as dt
from datetime import datetime
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_json_schema import JsonSchema
import flask_cors
from flask_socketio import SocketIO, emit
from json import dumps
from utils import json_serial

load_dotenv()

cors = flask_cors.CORS()
app = Flask(__name__)
SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret!'

app.config['JWT_SECRET_KEY'] = SECRET_KEY
app.config["JWT_TOKEN_LOCATION"] = ["headers", "query_string"]
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = dt.timedelta(days=1)
app.debug = True

jwt = JWTManager(app)
schema = JsonSchema(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Initializes CORS
cors.init_app(app)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/api/users/", methods=["POST"])
def add_user():
    try:
        user = request.json
        if not user:
            return {
                "message": "Please provide user details",
                "data": None,
                "error": "Bad request"
            }, 400
        is_validated = validate_user(user)
        if is_validated['ok'] is not True:
            return {
                "message": 'Invalid data',
                "data": None,
                "error": is_validated['message'].message,
            }, 400
        user = User().create(**user)
        if user == False:
            return {
                "message": "User with given email exists",
                "error": "User Exists",
                "data": None
            }, 409

        user["token"] = create_access_token(identity=user["email"])
        return {
            "message": "Successfully created new user",
            "data": user
        }, 201
    except Exception as e:
        return {
            "message": "Something went wrong",
            "error": str(e),
            "data": None
        }, 500


@app.route("/api/users/login", methods=["POST"])
def login():
    try:
        user = request.json
        if not user:
            return {
                "message": "Please provide user details",
                "data": None,
                "error": "Bad request"
            }, 400
        is_validated = validate_user(user)
        if is_validated['ok'] is not True:
            return {
                "message": 'Invalid data',
                "data": None,
                "error": is_validated['message'].message,
            }, 400
        user = User().login(
            user["email"],
            user["password"]
        )
        if user:
            try:
                # token should expire after 24 hrs
                user["token"] = create_access_token(identity=user["email"])
                return {
                    "message": "Successfully fetched auth token",
                    "data": user
                }
            except Exception as e:
                return {
                    "error": "Something went wrong",
                    "message": str(e)
                }, 500
        return {
            "message": "Invalid email or password",
            "data": None,
            "error": "Unauthorized"
        }, 401
    except Exception as e:
        return {
            "message": "Something went wrong!",
            "error": str(e),
            "data": None
        }, 500


@app.route("/api/users/", methods=["GET"])
@jwt_required()
def get_current_user():
    return jsonify({
        "message": "successfully retrieved user profile",
        "data": get_jwt_identity()
    })


@app.route("/api/chatlog/", methods=["GET"])
@jwt_required()
def get_chatlog():
    try:
        user_email = get_jwt_identity()
        chats = ChatLog().get_all_sorterd()
        return jsonify({"data": chats})
    except Exception as e:
        return {
            "error": "Something went wrong",
            "message": str(e)
        }, 500


@app.errorhandler(403)
def forbidden(e):
    return jsonify({
        "message": "Forbidden",
        "error": str(e),
        "data": None
    }), 403


@app.errorhandler(404)
def forbidden(e):
    return jsonify({
        "message": "Route Not Found!",
        "error": str(e),
        "data": None
    }), 404


@socketio.on("connect")
@jwt_required()
def connected():
    """event listener when client connects to the server"""
    print("client has connected")
    try:
        user_email = get_jwt_identity()
        ChatLog().create(text=user_email + " Joined the room", type="event",
                         timestamp=datetime.now(), user_email=user_email)
    except Exception as e:
        print(e)
    emit("connect", {"data": f"id: {request.sid} is connected"})


@socketio.on('data')
@jwt_required()
def handle_message(data):
    """event listener when client types a message"""
    print("data from front end ", data)
    try:
        chat = ChatLog().create(text=data, type="chat",
                                timestamp=datetime.now(), user_email=get_jwt_identity())
    except Exception as e:
        print(e)
        return {
            "error": "Something went wrong while creating chat!",
            "message": str(e)
        }, 500

    print(data)
    emit("data", {
        'text': data,
        'user_email': get_jwt_identity(),
        'timestamp': dumps(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), default=json_serial)
    }, broadcast=True)


@socketio.on("disconnect")
@jwt_required()
def disconnected():
    """event listener when client disconnects to the server"""
    print("user disconnected")
    try:
        user_email = get_jwt_identity()
        ChatLog().create(text=user_email + " Left the room", type="event",
                         timestamp=datetime.now(), user_email=user_email)
    except Exception as e:
        print(e)
    emit("disconnect", f"user {request.sid} disconnected", broadcast=True)


if __name__ == "__main__":
    socketio.run(app, debug=True, port=5000)
