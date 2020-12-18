  
from fastapi import Depends, FastAPI

from routers.user_router        import router as router_users  
from routers.transaction_router import router as router_transactions


app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost.tiangolo.com", "https://localhost.tiangolo.com",
    "http://localhost", "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware, allow_origins=origins,
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

# Incluimos nuestros dos endpoints en api 
app.include_router(router_users)
app.include_router(router_transactions)