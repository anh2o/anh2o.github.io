from routes.user_routes import user
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
async def home():
    return {"message": "Server Running"}
app.include_router(user)