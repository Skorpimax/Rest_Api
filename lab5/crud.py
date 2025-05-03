from bson import ObjectId
from fastapi.encoders import jsonable_encoder

from database import book_collection
from schemas import BookCreate, Book


async def create_book(book: BookCreate):
    book = jsonable_encoder(book)
    result = await book_collection.insert_one(book)
    return Book(id=str(result.inserted_id), **book)

async def get_books():
    books = []
    cursor = book_collection.find({})
    async for document in cursor:
        try:
            document["id"] = str(document["_id"])
            books.append(Book(**document))
        except Exception as e:
            print(e)
    return books

async def get_book(book_id: str):
    book = await book_collection.find_one({"_id": ObjectId(book_id)})
    if book:
        book["id"] = str(book["_id"])
        return book

async def delete_book(book_id: str):
    result = await book_collection.delete_one({"_id": ObjectId(book_id)})
    return result.deleted_count == 1
