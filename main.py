from db.user_db import UserInDB
from db.user_db import update_user, get_user
from db.transaction_db import TransactionInDB
from db.transaction_db import save_transaction
from models.user_models import UserIn, UserOut
from models.transaction_models import TransactionIn, TransactionOut
import datetime
from fastapi import FastAPI
from fastapi import HTTPException

api = FastAPI()

@api.post("/user/auth/")
async def auth_user(user_in: UserIn):

    user_in_db = get_user(user_in.username)

    if user_in_db == None:
        raise HTTPException(status_code=404, detail="El usuario no existe")

    if user_in_db.password != user_in.password:
        return {"Autenticado": False}

    return {"Autenticado": True}

@api.get("/user/balance/{username}")
async def get_balance(username: str):

    user_in_db = get_user(username)

    if user_in_db == None:
        raise HTTPException(status_code=404, detail="El usuario no existe")

    user_out = UserOut(**user_in_db.dict())
    return user_out

@api.put("/user/transaction/")
async def make_transaction(transaction_in: TransactionIn):

    user_in_db = get_user(transaction_in.username)

    if user_in_db == None:
        raise HTTPException(status_code=404, detail="El usuario no existe")

    if user_in_db.balance < transaction_in.value:
        raise HTTPException(status_code=400, detail="Sin fondos suficientes")

    user_in_db.balance = user_in_db.balance - transaction_in.value

    update_user(user_in_db)

    transaction_in_db = TransactionInDB(**transaction_in.dict(), actual_balance = user_in_db.balance)
    transaction_in_db = save_transaction(transaction_in_db)
    transaction_out = TransactionOut(**transaction_in_db.dict())

    return transaction_out






''' EJEMPLOS
app = FastAPI()


@app.get("/")           # GET / HTTP/1.1 (lado del cliente)
async def root():
    return {"Hello": "FastApi"}

@app.get("/users")      # GET /users HTTP/1.1 (lado del cliente)
async def users():
    return {"message": database_users}

@app.get("/users/{username}")      # GET /users HTTP/1.1 (lado del cliente)
async def get_user_username(username: str):
    if username in database_users:
        return {"message": database_users[username]}
    raise HTTPException(status_code=404, detail= "El usuario no existe")

@app.post("/users/")
async def create_user(user: UserInDB):
    database_users[user.username] = user
    return user

@app.delete("/users/")
async def delete_user(user: UserInDB):
    del database_users[user.username]
    return user

@app.put("/users/")
async def delete_user(user: UserInDB):
    database_users[user.username] = user
    return user
'''