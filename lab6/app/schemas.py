from marshmallow import Schema, fields, post_load

from .models import Book


class BookSchema(Schema):
    title = fields.Str(required=True)
    author = fields.Str(required=True)

    @post_load
    def make_book(self, data: dict, **kwargs):
        return Book(**data)

book_schema = BookSchema()
books_schema = BookSchema(many=True)