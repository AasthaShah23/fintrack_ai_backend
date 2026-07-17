from fastapi import FastAPI
from app.routes.auth import routes as auth_routes
from app.routes.categories import routes as category_routes
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

@app.get("/")
def root():
    return {"message": "API is running 🚀"}
