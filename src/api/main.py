from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

MONGO_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URL)
database = client["tai"]
collection = database["tasks"]

@app.get("/")
async def read_root():
    return await collection.find()


@app.get("/tasks/{item_id}")
async def read_item(item_id: int, q: str = None):
    return await collection.find_one({"_id": item_id})


@app.get("/tasks/add/{item_id}")
async def inser_item(item_id: int, q: str = None):
    await collection.insert_one({"_id": item_id})


@app.get("/tasks/delete/{item_id}")
async def delete_item(item_id: int, q: str = None):
    await collection.delete_one({"_id": item_id})

