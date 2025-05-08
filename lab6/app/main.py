from flask import Flask
from flasgger import Swagger
from flask_restful import Api

from .views import BookResource, BooksResource


def create_app():
    app = Flask(__name__)
    swagger = Swagger(app)
    api = Api(app)
    api.add_resource(BookResource, '/books/<string:book_id>')
    api.add_resource(BooksResource, '/books')
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)

