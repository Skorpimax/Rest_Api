from typing import Dict, Union
from app import db
from flask import Blueprint, jsonify, request, url_for

from .models import Book

main = Blueprint('main', __name__)


def make_response(data: Union[Dict, Book], status_code: int = 200):
    return jsonify(data), status_code

@main.route('/')
def index():
    return make_response("description", "Main page. There is nothing here")

@main.route("/books", methods=["GET"])
def get_books():
    limit = request.args.get('limit', default=3, type=int)
    cursor = request.args.get('cursor', default=None)
    direction = request.args.get('direction', default='desc', type=str)

    is_desc = direction == 'desc'

    my_query = Book.query.order_by(Book.id.desc() if is_desc else Book.id.asc())
    total = my_query.count()

    if cursor:
        if is_desc:
            my_query = my_query.filter(Book.id < int(cursor))
        else:
            my_query = my_query.filter(Book.id > int(cursor))

    books = my_query.limit(limit).all()

    if is_desc:
        books = sorted(books, key=lambda b: b.id, reverse=False)

    next_curs = books[-1].id if books else None
    prev_curs = books[0].id if books else None

    next_page = url_for('main.get_books', limit=limit, cursor=next_curs, direction='desc' if is_desc else 'asc') if next_curs else None
    prev_page = url_for('main.get_books', limit=limit, cursor=prev_curs, direction='asc' if is_desc else 'desc') if prev_curs else None

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
    book = Book(**data)
    db.session.add(book)
    db.session.commit()
    return make_response({"book": (book.to_dict())}, 201)

@main.route('/books/<string:id>', methods=['DELETE'])
def delete_book(id: str):
    book = Book.query.get_or_404(id, description="Book is not found")

    db.session.delete(book)
    db.session.commit()

    return make_response({"message": "Book deleted"}, 200)
