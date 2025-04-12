from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def handle_404(err):
    return ({"error": "Not Found"}, 404)


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@db:3306/booksdb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .views import main
    app.register_blueprint(main, url_prefix='/v1/api')
    app.register_error_handler(404, handle_404)

    return app