from fastapi import FastAPI
import user_account,user_profile
from db.db_conn import conn




app = FastAPI()

app.include_router(user_profile.user)
app.include_router(user_account.user)

@app.get('/')
def test():
    return "Hello World"

