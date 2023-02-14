from fastapi import APIRouter, Request
import bcrypt
from db import user_db, validate, user_session

user = APIRouter(
    prefix='/api/account',
    )
# Create a new user route
@user.get('/create/{username}/{email}/{password}')
def create_user(username, email, password, request: Request):
    print(request.headers)
    # Check if the username, email and password are valid using the ./db/validate.py file
    if not validate.validate_username(username) and validate.validate_mail(email) and validate.validate_pass(password):
        return {"error": "Invalid username, email or password"}, 400
    
    # Check if the email address is already in use 
    elif user_db.email_exists(email):
       return {"error": "Email address already in use"}, 400
    else:
        # Hash the password using bcrypt
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        # Create the user in the database
        user_db.create_user(username, email, password_hash)
        # logsin the user and return the session token
        session_token = user_session.login(email, password)
        return {"message": "User created successfully","sesion_token": str(session_token)}, 200


# Login route
@user.get('/login/{email}/{password}')
def login(email, password):
    # log in the user and return the session token if login successful
    login = user_session.login(email, password)
    session_token = login[0] 
    
    if session_token:
        return {"session_token": session_token,"user_id":login[1]}, 200
    else:
        return {"error": "Invalid email or password"}, 400
    
@user.get('/logout/{user_id}')
def logout(user_id, request: Request):
    session_token = request.headers.get('session_token')
    if not session_token:
        return {"error": "Missing session token"}, 400
    # Check if the session token is valid and for the correct user
    if not user_session.get_user_from_session_token(session_token) or not user_session.get_user_from_session_token(session_token)["user_id"] == user_id:
        return {"error": "Invalid session token"}, 400
    
    user_session.logout(session_token)
    return {"message": "Logged out successfully"}, 200

@user.post("/follow/{user_id}/{follow_id}")
def follow(user_id, follow_id, request: Request):
    session_token = request.headers.get('session_token')
    user_data = user_session.get_user_from_session_token(session_token)
    if not user_data:
        # Return an error if the session token is not valid
        return {"error": "Invalid session token"}, 401
    if user_db.follow(user_id, follow_id):
        return {"message": "Followed successfully"}, 200
    else:
        return {"error": "User not found"}, 404

@user.post("/unfollow/{user_id}/{follow_id}")
def unfollow(user_id, follow_id, request: Request):
    session_token = request.headers.get('session_token')
    user_data = user_session.get_user_from_session_token(session_token)
    if not user_data:
        # Return an error if the session token is not valid
        return {"error": "Invalid session token"}, 401
    if user_db.unfollow(user_id, follow_id):
        return {"message": "Unfollowed successfully"}, 200
    else:
        return {"error": "User not found"}, 404