import os

from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()

mongodb_url = os.getenv("MONGODB_URL")

if not mongodb_url:
    raise RuntimeError(
        "MONGODB_URL is missing. Add it to your .env file."
    )

client = MongoClient(
    mongodb_url,
    serverSelectionTimeoutMS=5000,
)

database = client["learning_cloud"]
tasks_collection = database["tasks"]