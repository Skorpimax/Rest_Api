import os

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

client = AsyncIOMotorClient(os.getenv('MONGODB_URL'))
db = client.bookstore
book_collection = db.get_collection("books")