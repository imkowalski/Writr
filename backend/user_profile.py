from fastapi import APIRouter, Request

from db import user_db, user_session,post_db
'''
In this file we will define the api endpoints for getting the user profile information
'''


from pydantic import BaseModel


class Post(BaseModel):
    content: str



# define the router for the user profile (fastapi)
user = APIRouter(
    prefix='/api/user',
    )


# get the raw user information
@user.get('/get/info/{user_id}')
def get_user(user_id, request: Request):
    session_token = request.headers.get('session_token')
    user_data = user_session.get_user_from_session_token(session_token)
    print(request.headers)
    if not user_data:
        # Return an error if the session token is not valid
        return {"error": "Invalid session token"}, 401
    user = user_db.get_user(user_id)
    
    user.pop("password_hash".encode("utf-8"))
    
    if user:
        return user, 200
    else:
        return {"error": "User not found"}, 404



# get alll user information including latest 40 posts, followers and following
@user.get('/get/all/{user_id}')
def get_all_user(user_id, request: Request):
    session_token = request.headers.get('session_token')
    user_data = user_session.get_user_from_session_token(session_token)

    if not user_data:
        # Return an error if the session token is not valid
        return {"error": "Invalid session token"}, 401
    user = user_db.get_user(user_id)
    last_40_posts = post_db.get_user_posts(user_id)
    followers = user_db.get_followers(user_id)
    following = user_db.get_following(user_id)
    if user:
        return {"user": user,"posts":last_40_posts,"followers":followers,"following":following}, 200
    else:
        return {"error": "User not found"}, 404


# get the user followers
@user.get('/get/followers/{user_id}')
def get_followers(user_id, request: Request):
    session_token = request.headers.get('session_token')
    user_data = user_session.get_user_from_session_token(session_token)

    if not user_data:
        # Return an error if the session token is not valid
        return {"error": "Invalid session token"}, 401
    followers = user_db.get_followers(user_id)
    if followers:
        return {"followers": followers}, 200
    else:
        return {"error": "User not found"}, 404

@user.get('/get/following/{user_id}')
def get_following(user_id, request: Request):
    session_token = request.headers.get('session_token')
    user_data = user_session.get_user_from_session_token(session_token)

    if not user_data:
        return {"error": "Invalid session token"}, 401
    following = user_db.get_following(user_id)
    if following:
        return {"following": following}, 200
    else:
        return {"error": "User not found"}, 404

@user.get('/get/usernames/{user_id}')
def get_usernames(user_id, request: Request):
    return {"usernames": user_db.get_usernames(user_id)}, 200

@user.get('/get/posts/{user_id}')
def get_posts(user_id, request: Request):
    session_token = request.headers.get('session_token')
    user_data = user_session.get_user_from_session_token(session_token)

    if not user_data:
        return {"error": "Invalid session token"}, 401
    posts = post_db.get_user_posts(user_id)
    if posts:
        return {"posts": posts}, 200
    else:
        return {"error": "User not found"}, 404

@user.get('/get/posts/for_home/{user_id}')
def get_posts_for_home(user_id, request: Request):
    session_token = request.headers.get('session_token')
    user_data = user_session.get_user_from_session_token(session_token)

    if not user_data:
        return {"error": "Invalid session token"}, 401
    
    posts = post_db.get_following_posts(user_id)
    
    if posts:
        return {"posts": posts}, 200
    else:
        return {"error": "User not found","sd":posts}, 404

@user.post('/create/post/{user_id}')
def create_post(user_id, content: Post, request: Request):
    session_token = request.headers.get('session_token')
    user_data = user_session.get_user_from_session_token(session_token)

    if not user_data:
        return {"error": "Invalid session token"}, 401
    post = post_db.create_post(user_id, content.content)
    if post:
        return {"post": post}, 200
    else:
        return {"error": "User not found"}, 404