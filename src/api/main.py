from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MONGO_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URL)
database = client["tai"]
collection = database["tasks"]


class Task(BaseModel):
    _id: int
    title: str


@app.get("/tasks")
async def read_tasks():
    data = []
    async for item in collection.find():
        print(item)
        data.append(item)
    return data


@app.get("/tasks/{item_id}")
async def read_task(item_id: int, q: str = None):
    return collection.find_one({"_id": item_id});


@app.post("/tasks")
async def insert_task(task: Task):
    await collection.insert_one({"_id": await get_max_id() + 1, "title": task.title})


@app.put("/tasks/{item_id}")
async def edit_task(item_id: int, task: Task):
    await collection.find_one_and_update({"_id": item_id}, {'$set': {"title": task.title}})


@app.delete("/tasks/{item_id}")
async def delete_task(item_id: int):
    await collection.find_one_and_delete({"_id": item_id})


async def get_max_id():
    max_id_document = await collection.find_one(
        filter={},
        sort=[("_id", -1)],
    )
    if max_id_document is None:
        return 0
    return max_id_document['_id'];
