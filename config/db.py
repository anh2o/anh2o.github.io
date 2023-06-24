from pymongo import MongoClient
db_connection = MongoClient("mongodb+srv://korolevkonstantinv:A6x554hGqGBfKswn@cluster0.bdbme88.mongodb.net/?retryWrites=true")
db = db_connection.Users
collection = db["TEST"]