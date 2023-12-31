from fastapi import APIRouter
from models.user_model import User
from schemas.user_schema import users_serializer
from bson import ObjectId
from config.db import collection
import plotly.express as px

user = APIRouter()

@user.post("/")
async def create_user(user: User):
    _id = collection.insert_one(dict(user))
    user = users_serializer(collection.find({"_id": _id.inserted_id}))
    return {"status": "Ok","data": user}

@user.get("/")
async def find_all_users():
    users = users_serializer(collection.find())
    return {"status": "Ok","data": users}
            
@user.get("/{id}")
async def get_one_user(id: str):
   user = users_serializer(collection.find({"tgid": str(id)}))
   return {"status": "Ok","data": user}

@user.put("/{id}")
async def update_user(id: str, user: User):
    collection.find_one_and_update(
        {
          "tgid": id
        }, 
        {
         "$set": dict(user)
        })
    user = users_serializer(collection.find({"tgid": id}))
    return {"status": "Ok","data": user}

@user.delete("/{id}")
async def delete_user(id: str):
   collection.find_one_and_delete({"tgid": id})
   users = users_serializer(collection.find())
   return {"status": "Ok","data": []} 

async def create_user_page(user:User):
    df = px.data.tips()
    fig = px.pie(df, values='tip', names='day')
    fig.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    fig.write_html(f"{user.tgid}.html",default_height='50%')