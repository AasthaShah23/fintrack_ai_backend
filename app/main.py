from fastapi import FastAPI
from app.routes.auth import routes as auth_routes
from app.routes.categories import routes as category_routes
from app.routes.budget import routes as budget_routes
from app.routes.transactions import routes as transaction_routes
from app.routes.dasboard import routes as dasboard_routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(category_routes.router)
app.include_router(budget_routes.router)
app.include_router(transaction_routes.router)
app.include_router(dasboard_routes.router)
@app.get("/")
def root():
    return {"message": "API is running 🚀"}
