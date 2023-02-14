import uuid
import bcrypt
from db.db_conn import conn

# Login a user
def login(email, password):
    # Get the user id from the email address
    user_id = conn.hget("email_to_user_id", email)

    # If the user id is not found return None
    if not user_id:
        return None
    
    # Get the password hash from the user id
    stored_password = conn.hget("user:" + str(user_id.decode('utf-8')), "password_hash")

    # If the password hash is not found return None
    if not bcrypt.checkpw(str(password).encode('utf-8'), stored_password):
        return None
    
    # Create a session token
    session_token = str(uuid.uuid4())
    conn.hmset("session:" + session_token, {
        "user_id": user_id,
        "email": email
    })
    conn.expire("session:" + session_token, 120 * 60)

    return (session_token, user_id)


# Get the user id from the session token
def get_user_from_session_token(session_token):
    session_data = conn.hgetall("session:" + session_token)
    if not session_data:
        return None
    conn.expire("session:" + session_token, 30 * 60)
    return session_data

# Logout a user by deleting the session token from Redis
def logout(session_token):
    # Delete the session token from Redis
    conn.delete("session:" + session_token)