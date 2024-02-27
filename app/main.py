import json

from fastapi import Cookie, FastAPI, Form, Request, Response, templating, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from typing import List
import bcrypt
from starlette.responses import JSONResponse

from .flowers_repository import Flower, FlowersRepository
from .purchases_repository import Purchase, PurchasesRepository
from .users_repository import User, UsersRepository

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

templates = templating.Jinja2Templates("templates")

flowers_repository = FlowersRepository()
purchases_repository = PurchasesRepository()
users_repository = UsersRepository()


async def get_cart_from_cookies(cart_cookie: str = Cookie(default="")):
    return [int(item_id) for item_id in cart_cookie.split(",") if item_id]


async def set_cart_to_cookies(cart: List[int]):
    return ",".join(str(item_id) for item_id in cart)


@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/users")
def print_users(request: Request):
    users = users_repository.get_users()

    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.get("/user/{email}")
def user(request: Request, email):
    us = users_repository.get_user(email)
    return templates.TemplateResponse("user.html", {"request": request, "user": us})


# ваше решение сюда

def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password


def password_match(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password)


@app.get("/signup")
def signUpGet(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@app.post("/signup")
async def do_signup(request: Request, fname: str = Form(...), lname: str = Form(...), email: str = Form(...),
                    password: str = Form(...)):
    if users_repository.get_user(email) is not None:
        raise HTTPException(status_code=400, detail="User already registered")
    hashed = hash_password(password)
    full_name = f"{fname} {lname}"
    users_repository.add_user(email, full_name, hashed)
    # return {'message': 'User registered successfully!'}
    return RedirectResponse(url="/login", status_code=303)


@app.get("/login")
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
def login(request: Request, email: str = Form(...), password: str = Form(...)):
    actual_password = users_repository.get_password(email)
    users = users_repository.get_users()

    if actual_password is not None and password_match(password, actual_password):
        return RedirectResponse(f"/user/{email}", status_code=303)
    else:
        return templates.TemplateResponse("login.html", {"request": request, "message": "wrong password"})


@app.get("/flowers")
def get_flowers():
    return flowers_repository.__json__()


@app.post("/flowers")
def add_flower(flower_request):
    json_request = json.loads(flower_request)
    new_flower = Flower(name=json_request["name"], count=json_request["count"], cost=json_request["cost"], id=0)
    flower_id = flowers_repository.add(new_flower)
    return {"id": flower_id}


@app.post("/cart/items")
async def add_item_to_cart(flower_id: int = Form(...), cart_cookie: str = Cookie(default="")):
    cart = [int(item_id) for item_id in cart_cookie.split(",") if item_id]
    for flower in flowers_repository.get_flowers():
        if flower_id == flower.id:
            flowers_repository.add_to_cart(flower)
            response = JSONResponse({"message": f"Item with id {flower_id} added to cart"})
            response.set_cookie(key="cart", value=",".join(str(item_id) for item_id in cart))
            return response
    return {"message": "Flower not found"}, 404


# Get items in cart
@app.get("/cart/items")
async def get_items_in_cart(cart: List[int] = Depends(get_cart_from_cookies)):
    return flowers_repository.__jsonCart__()

# конец решения
