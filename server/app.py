#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_restful import Api, Resource
from flask_migrate import Migrate

from models import db, Author, Publisher, Book

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

@app.get('/')
def index():
    return "Hello world"

# write your routes here!

if __name__ == '__main__':
    app.run(port=5555, debug=True)

@app.route('/authors/<int:id>', methods = ['GET', 'DELETE'])
def author_by_id(id):
    author = Author.query.filter(Author.id == id).first()

    if author:
        if request.method == 'GET':
            response = make_response(
                {
                    'id': author.id,
                    'name': author.name,
                    'pen_name': author.pen_name,
                    'books': [book.to_dict(rules = '-books', ) for book in author.books]
                },
                200
            )
        elif request.method == 'DELETE':
            assoc_books = Book.query.filter(Book.author_id == id).all()

            for assoc_book in assoc_books:
                db.session.delete(assoc_book)

            db.session.delete(author)
            db.session.commit()

            response = make_response(
                {},
                204
            )
    else:
        response = make_response(
            { 'error': 'Author not found' },
            404
        )
    
    return response

@app.route('/books', methods = ['GET', 'POST'])
def books():
    if request.method == 'GET':
        books = Book.query.all()

        books_dict = [book.to_dict() for book in books]

        response = make_response(
            books_dict,
            200
        )
    elif request.method == 'POST':
        try:
            form_data = request.get_json()

            new_book = Book(
                title = form_data['title'],
                page_count = form_data['page_count']
            )

            db.session.add(new_book)
            db.session.commit()

            response = make_response(
                new_book.to_dict(),
                201
            )
        except ValueError:
            response = make_response(
                { 'errors': ['validation errors'] },
                400
            )

    return response

@app.route('/publishers/<int:id>', methods = ['GET'])
def publisher_by_id(id):
    publisher = Publisher.query.filter(Publisher.id == id).first()

    if publisher:
        response = make_response(
            publisher.to_dict(),
            200
        )
    else:
        response = make_response(
            { 'error': 'publisher not found' },
            404
        )
    
    return response
