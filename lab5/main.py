from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException

import crud
from schemas import Book, BookCreate

app = FastAPI()
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, debug=True)

@app.get("/")
async def root():
    return {"message": "Welcome to the Book API!"}

@app.post("/books", response_model=Book)
async def create_book(book: BookCreate):
    return await crud.create_book(book)

@app.get("/books", response_model=List[Book])
async def get_books():
    return await crud.get_books()

@app.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: str):
    book = await crud.get_book(book_id)
    if book:
        return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/{book_id}")
async def delete_book(book_id: str):
    deleted = await crud.delete_book(book_id)
    if deleted:
        return {"message": "Book deleted"}
    raise HTTPException(status_code=404, detail="Book not found")