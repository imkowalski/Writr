from fastapi import FastAPI, Form, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import requests

b_url = "http://127.0.0.1:8000"


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/profile/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/login")
def get_login(request: Request):
    return templates.TemplateResponse("login.html",{"request":request,"title":"Login"})

@app.post("/login")
async def login(request: Request, response: Response, email: str = Form(), password: str = Form()):
    r = requests.get(b_url + f"/api/account/login/{email}/{password}")
    
    if r.json()[1] == 400:
        return templates.TemplateResponse("login.html",{"request":request,"title":"Login","error":r.json()[0]["error"]})
    res = RedirectResponse(url="/")
    res.set_cookie(key="session_token",value=r.json()[0]["session_token"])
    res.set_cookie(key="user_id",value=r.json()[0]["user_id"])
    return res


@app.get("/register", response_class=RedirectResponse)
def get_register(request: Request):
    return templates.TemplateResponse("register.html",{"request":request,"title":"Register"})

@app.post("/register", response_class=RedirectResponse)
async def register(request: Request, response: Response, email: str = Form(), password: str = Form(), username: str = Form()):
    r = requests.get(b_url + f"/api/account/create/{username}/{email}/{password}")
    print(r.json())
    if r.json()[1] == 400:
        return templates.TemplateResponse("register.html",{"request":request,"title":"Register","error":r.json()[0]["error"]})
    r_l = requests.get(b_url + f"/api/account/login/{email}/{password}")
    res = RedirectResponse(url="/")
    res.set_cookie(key="session_token",value=r_l.json()[0]["session_token"])
    res.set_cookie(key="user_id",value=r_l.json()[0]["user_id"])
    return res


@app.post("/myprofile")
@app.get("/myprofile")
def get_myprofile(request: Request):
    user_id = request.cookies["user_id"]
    session_token = request.cookies["session_token"]
    r = requests.get(b_url + f"/api/user/get/all/{user_id}",headers={"session_token":session_token})
    return templates.TemplateResponse("profile.html",{
        "request":request,
        "title":"Profile",
        "user":r.json()[0]["user"],
        "user_id":user_id,
        "posts":r.json()[0]["posts"],
        "following":len(r.json()[0]["followers"]),
        "followers":len(r.json()[0]["following"]),
        "myprofile":True
        })

@app.post("/profile/{user_id}")
@app.get("/profile/{user_id}")
def get_profile(request: Request, user_id):
    session_token = request.cookies["session_token"]
    r = requests.get(b_url + f"/api/user/get/all/{user_id}",headers={"session_token":session_token})
    return templates.TemplateResponse("profile.html",{
        "request":request,
        "title":"Profile",
        "user":r.json()[0]["user"],
        "user_id":user_id,
        "posts":r.json()[0]["posts"],
        "following":len(r.json()[0]["followers"]),
        "followers":len(r.json()[0]["following"]),
        "user_is_following":False,
        "myprofile":False
        })

@app.post("/create_post")
def create_post(request: Request, response: Response, post_content: str = Form()):
    user_id = request.cookies["user_id"]
    session_token = request.cookies["session_token"]
    requests.post(b_url + f"/api/user/create/post/{user_id}",headers={"session_token":session_token},json={"content":str(post_content)})
    return RedirectResponse("/myprofile")

@app.post("/profile/{follow_id}/follow")
def follow_user(request: Request, response: Response, follow_id):
    session_token = request.cookies["session_token"]
    user_id = request.cookies["user_id"]
    r = requests.post(b_url + f"/api/account/follow/{user_id}/{follow_id}",headers={"session_token":session_token})
    return RedirectResponse(f"/profile/{follow_id}")



@app.get("/")
@app.post("/")
@app.get("/home")
@app.post("/home")
def get_home(request: Request):
    try:
        session_token = request.cookies["session_token"]
        user_id = request.cookies["user_id"]
        r = requests.get(b_url + f"/api/user/get/posts/for_home/{user_id}",headers={"session_token":session_token})
        return templates.TemplateResponse("home.html",{"request":request,"title":"Home","posts":r.json()[0]["posts"]})
    except Exception as KeyError:
        print(KeyError)
        return templates.TemplateResponse("welcome.html",{"request":request,"title":"Welcome"})


