from typing import Dict, Union
from app import db
from flask import Blueprint, jsonify, abort, request, url_for

from .models import Book

main = Blueprint('main', __name__)


def make_response(data: Union[Dict, Book], status_code: int = 200):
    return jsonify(data), status_code

@main.route('/')
def index():
    return make_response("description", "Main page. There is nothing here")

@main.route("/books", methods=["GET"])
def get_books():
    limit = request.args.get('limit', default=10, type=int)
    offset = request.args.get('offset', default=0, type=int)

    books = Book.query.offset(offset).limit(limit).all()
    total = Book.query.count()

    next_page = url_for('books.get_books', limit=limit, offset=offset + limit) if offset + limit < total else None
    prev_page = url_for('books.get_books', limit=limit, offset=max((offset - limit), 0)) if offset > 0 else None

    return make_response({"books": [b.to_dict() for b in books],
                          "total amount": total,
                          "next page": next_page,
                          "previous page": prev_page})

@main.route("/books/<string:id>", methods=["GET"])
def get_book(id):
    book = Book.query.get_or_404(id)
    return make_response({"book": book.to_dict()})

@main.route("/books", methods=["POST"])
def create_book():
    data = request.get_json()
    book = Book(title=data['title'], author=data['author'])
    db.session.add(book)
    db.session.commit()
    return make_response({"book": (book.to_dict())}, 201)

@main.route('/books/<string:id>', methods=['DELETE'])
def delete_book(id: str):
    book = Book.query.get_or_404(id, description="Book is not found")

    db.session.delete(book)
    db.session.commit()

    return make_response({"message": "Book deleted"}, 200)