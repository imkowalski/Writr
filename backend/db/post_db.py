import time
from db.db_conn import conn

'''
In this file there are functions that are used to create, get and delete posts and comments in the database.
'''

# Get all posts made by all users (DO NOT USE THIS FUNCTION IN PRODUCTION)
def get_all_posts():
    post_ids = conn.lrange("posts", 0, -1)
    posts = []
    for post_id in post_ids:
        post = conn.hgetall("post:" + str(post_id))
        posts.append(post)
    return list(reversed(posts))


# Create a post
def create_post(user_id, content):
    post_id = conn.incr("next_post_id")
    timestamp = int(time.time())
    print(content)
    conn.hmset("post:" + str(post_id), {
        "user_id": user_id,
        "content": content,
        "timestamp": timestamp
    })
    conn.lpush("posts", post_id)
    conn.lpush("user:" + str(user_id) + ":posts", post_id)
    return post_id


# Get a specific post made by a specific user
def get_user_post( user_id, post_id):
    post = conn.hgetall("post:" + str(post_id))
    if post['user_id'] == str(user_id):
        return post
    else:
        return None

# get a post by its id
def get_post(post_id):
    return conn.hgetall("post:" + str(post_id))

# Get count(40 by default) posts made by a user
def get_user_posts(user_id, index=0, count=40):
    post_ids = conn.lrange("user:" + str(user_id) + ":posts", index, index + count - 1)
    posts = []
    for post_id in post_ids:
        post_data = conn.hgetall("post:" + str(post_id.decode('utf-8')))
        posts.append(post_data)

    return posts


# Get the next count(40 by default) posts made by the users that the user with user_id follows
# the offset parameter is used to get the next count(40 by default) posts
def get_following_posts(user_id, offset=0,count=40):
    if not conn.exists("followers:" + str(user_id)):
        return {"Error": "User does not exist"}
    
    
    following = conn.smembers("followers:"+str(user_id))
    # Retrieve the next 40 posts for each user
    posts = []
    for followed_user_id in following:
        followed_user_posts = conn.lrange("user:" + str(followed_user_id.decode('utf-8')) + ":posts", offset, offset + (count - 1))
        for post_id in followed_user_posts:
            post = conn.hgetall("post:" + str(post_id.decode('utf-8')))
            post["username"] = conn.hget("user:" + str(followed_user_id.decode('utf-8')), "username")
            post["post_id"] = post_id.decode('utf-8')
            posts.append(post)
            

    sorted_posts = sorted(posts, key=lambda k: k['timestamp'.encode()].decode(), reverse=True)
    # Sort the posts by timestamp
    return sorted_posts[:40]
