from pydantic import BaseModel

class BookInDB(BaseModel):
    title: str
    author: str

class Book(BookInDB):
    id: str