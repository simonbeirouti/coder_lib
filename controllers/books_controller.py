from flask import Blueprint, jsonify, request
from main import db
from models.books import Book
from schemas.book_schema import book_schema, books_schema
from flask_jwt_extended import jwt_required, get_jwt_identity

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
@jwt_required()
def new_book():
    if get_jwt_identity() != "librarian":
        return {"error": "Only librarians can add books."}, 403
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

@books.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_book(id):
    if get_jwt_identity() != "librarian":
        return {"error": "Only librarians can delete books."}, 403
    book = Book.query.get(id)
    if not book:
        return {"error": "Book id not found."}, 404
    db.session.delete(book)
    db.session.commit()
    return jsonify(book_schema.dump(book))

@books.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_book(id):
    if get_jwt_identity() != "librarian":
        return {"error": "Only librarians can update books."}, 403
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