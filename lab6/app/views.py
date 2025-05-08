from flask_restful import Resource
from typing import Dict, Union

from flask import abort, request
from flasgger import Swagger, swag_from
from marshmallow import ValidationError

from .models import Book, books
from .schemas import BookSchema, book_schema, books_schema


def get_book_by_id(id) -> Union[Book, None]:
    for book in books:
        if book.id == id:
            return book

class BookResource(Resource):
    @swag_from({
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'type': 'string',
                'required': True,
                'description': 'Book id'
            }
        ],
        'responses': {
            200: {
                'description': 'Book found',
                'examples': {
                    'application/json': {
                        'book': {
                            'title': 'Example Book',
                            'author': 'Example Author'
                        }
                    }
                }
            },
            404: {
                'description': 'Book not found',
                'examples': {
                    'application/json': {
                        'error': 'Book not found'
                    }
                }
            }
        }
    })
    def get(self, book_id: str):
        book = get_book_by_id(book_id)
        if not book:
            return abort(404)
        return {"book": book_schema.dump(book)}, 200


    @swag_from({
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'type': 'string',
                'required': True,
                'description': 'Book id'
            }
        ],
        'responses': {
            204: {
                'description': 'Book deleted',
            },
            404: {
                'description': 'Book not found',
                'examples': {
                    'application/json': {
                        'error': 'Book not found'
                    }
                }
            }
        }
    })
    def delete(self, book_id: str):
        book = get_book_by_id(book_id)
        if not book:
            return abort(404)
        books.remove(book)
        return {}, 204

class BooksResource(Resource):
    @swag_from({
        'responses': {
            200: {
                'description': 'Books found',
                'examples': {
                    'application/json': {
                        "books" :
                            [
                                {
                                    'title': 'Example Book',
                                    'author': 'Example Author'
                                },
                                {
                                    'title': 'Example Book2',
                                    'author': 'Example Author2'
                                }
                            ]

                    }
                }
            },
        }
    })
    def get(self):
        return {"books": books_schema.dump(books)}, 200

    @swag_from({
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'title': {
                            'type': 'string',
                            'example': 'The Book Title'
                        },
                        'author': {
                            'type': 'string',
                            'example': 'The Book Author'
                        }
                    },
                    'required': ['title', 'author']
                }
            }
        ],
        'responses': {
            201: {
                'description': 'Book created',
                'examples': {
                    'application/json': {
                        "book": {
                            "author": "The Book Author",
                            "id": "The book id",
                            "title": "The Book Title"
                        }
                    }
                }
            },
            422: {
                'description': 'Validation Error',
                'examples': {
                    'application/json': {
                        'error': {
                            'title': ['Missing data for required field.']
                        }
                    }
                }
            }
        }
    })
    def post(self):
        data = request.get_json()
        try:
            book = book_schema.load(data)
        except ValidationError as err:
            return {"error": err.messages}, 422
        books.append(book)
        return {"book": book_schema.dump(book)}, 201