from db.db_conn import conn


# Create a new user
def create_user(username, email, password):
    user_id = conn.incr("next_user_id")
    conn.hmset("user:" + str(user_id), {
        "username": username,
        "email": email,
        "password_hash": password,
    })
    conn.sadd("email_addresses", email)
    conn.sadd("usernames", username)
    conn.hset("email_to_user_id", email, user_id)
    conn.set("username_to_user_id:" + username, user_id)
    return user_id

# Checks if an email address is already in use
def email_exists(email):
    return conn.sismember("email_addresses", email)

# Gets a user by their username 
def get_user_by_username(username):
    if conn.sismember("usernames", username):
        user_id = int(conn.get("username_to_user_id:" + username))
        return conn.hgetall("user:" + str(user_id))
    else:
        return None

# Gets a user by their username
def get_user_id_by_username(username):
    if conn.sismember("usernames", username):
        user_id = int(conn.get("username_to_user_id:" + username))
        return user_id
    else:
        return None


# Gets a user by their user id
def get_user(user_id):
    return conn.hgetall("user:" + str(user_id))


# Follows a user
def follow(user_id, follow_id):
    conn.sadd("followers:" + str(user_id), follow_id)
    conn.sadd("followings:" + str(follow_id), user_id)

# Unfollows a user
def unfollow( user_id, follow_id):
    # Remove the follow_id from the set of the user's followers with the key "followers:<user_id>"
    conn.srem("followers:" + str(user_id), follow_id)
    # Remove the user_id from the set of the follow_id's followings with the key "followings:<follow_id>"
    conn.srem("followings:" + str(follow_id), user_id)

# Gets a user's followers
def get_followers( user_id):
    return conn.smembers("followers:" + str(user_id))

# Gets a user's followings
def get_following( user_id):
    return conn.smembers("followings:" + str(user_id))


def is_following(user_id, follow_id):
    return conn.sismember("followers:" + str(user_id), follow_id)











