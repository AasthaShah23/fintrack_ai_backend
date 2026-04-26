from fastapi import FastAPI
from app.routes.auth import routes

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API is running 🚀"}

app.include_router(routes.router)