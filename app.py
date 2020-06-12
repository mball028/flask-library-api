from flask import Flask, jsonify, request
import os
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + \
    os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
marsh = Marshmallow(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    author = db.Column(db.String(100))

    def __init__(self, title, author):
        self.title = title
        self.author = author


class BookSchema(marsh.Schema):
    class Meta:
        fields = ('id', 'title', 'author')


book_schema = BookSchema()
books_schema = BookSchema(many=True)


@app.route('/')
def server_on():
    return 'Flask Library Server is running.'


@app.route('/books', methods=['GET'])
def get_books():
    all_books = Book.query.all()
    if len(all_books) < 1:
        return 'No books currently in database.'
    books = books_schema.dump(all_books)
    return jsonify(books)


@app.route('/books/<id>', methods=['GET'])
def get_book(id):
    book = Book.query.get(id)
    return book_schema.jsonify(book)


@app.route('/books/add', methods=['POST'])
def add_book():
    title = request.json['title']
    author = request.json['author']

    new_book = Book(title, author)

    db.session.add(new_book)
    db.session.commit()

    return f'{title} by {author} successfully added to the library.'


@app.route('/books/update/<id>', methods=['PUT'])
def update_book():
    book = Book.query.get(id)

    title = request.json['title']
    author = request.json['author']

    book.title = title
    book.author = author

    db.session.commit()

    return f'{book.title} successfully updated.'


@app.route('/books/remove/<id>', methods=['DELETE'])
def delete_book():
    book = Book.query.get(id)

    db.session.delete(book)
    db.session.commit()
    return f'{book.title} has been removed from the library.'


if __name__ == '__main__':
    app.run(debug=True)
