from flask import Blueprint, jsonify, request
from main import db
from models.books import Book
from schemas.book_schema import book_schema, books_schema

books = Blueprint("books", __name__, url_prefix="/books")

@books.route("/", methods=["GET"])
def get_books():
    books_list = Book.query.all()
    result = books_schema.dump(books_list)
    return result

@books.route("/<int:id>", methods=["GET"])
def get_book(id):
    book = Book.query.get(id)
    result = book_schema.dump(book)
    return result

@books.route("/", methods=["POST"])
def new_book():
    book_fields = book_schema.load(request.json)
    book = Book(
        title = book_fields["title"],
        genre = book_fields["genre"],
        year = book_fields["year"],
        length = book_fields["length"]
    )
    db.session.add(book)
    db.session.commit()
    return jsonify(book_schema.dump(book))

# delete book
@books.route("/<int:id>", methods=["DELETE"])
def delete_book(id):
    book = Book.query.get(id)
    if not book:
        return {"error": "Book id not found."}, 404
    db.session.delete(book)
    db.session.commit()
    return jsonify(book_schema.dump(book))

@books.route("/<int:id>", methods=["PUT"])
def update_book(id):
    book = Book.query.get(id)
    if not book:
        return {"error": "Book id not found."}, 404
    book_fields = book_schema.load(request.json)
    book.title = book_fields["title"]
    book.genre = book_fields["genre"]
    book.year = book_fields["year"]
    book.length = book_fields["length"]
    db.session.commit()
    return jsonify(book_schema.dump(book))