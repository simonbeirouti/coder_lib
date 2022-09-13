from flask import Blueprint, jsonify, request
from main import db
from models.books import Book
from models.reservation import Reservation
from models.users import User
from schemas.book_schema import book_schema, books_schema
from schemas.reservation_schema import reservation_schema, reservations_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import date

books = Blueprint("books", __name__, url_prefix="/books")

@books.route("/", methods=["GET"])
def get_books():
    if request.query_string:
        if request.args.get("genre"):
            filtered_list = Book.query.filter_by(genre = request.args.get("genre"))
            result = books_schema.dump(filtered_list)
            return result, 200
        elif request.args.get("author"):
            filtered_list = Book.query.filter_by(author = request.args.get("author"))
            result = books_schema.dump(filtered_list)
            return result, 200
        elif request.args.get("title"):
            filtered_list = Book.query.filter_by(title = request.args.get("title"))
            result = books_schema.dump(filtered_list)
            return result, 200
        elif request.args.get("year"):
            filtered_list = Book.query.filter_by(year = request.args.get("year"))
            result = books_schema.dump(filtered_list)
            return result, 200
        else:
            return {"message": "Invalid query string"}, 400
    books_list = Book.query.all()
    result = books_schema.dump(books_list)
    return result, 200

@books.route("/<int:id>", methods=["GET"])
def get_book(id):
    book = Book.query.get(id)
    result = book_schema.dump(book)
    return result, 200

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
        length = book_fields["length"],
        author_id = book_fields["author_id"]
    )
    db.session.add(book)
    db.session.commit()
    return jsonify(book_schema.dump(book)), 201

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
    return jsonify(book_schema.dump(book)), 201

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
    return jsonify(book_schema.dump(book)), 201

@books.route("/reservations", methods=["GET"])
@jwt_required()
def get_all_reservations():
    if get_jwt_identity() != "librarian":
        return {"error": "Only librarians can view books with reservations."}, 403
    reservation_list = Reservation.query.all()
    result = reservations_schema.dump(reservation_list)
    return result, 201

@books.route("/<int:book_id>/reservations", methods=["POST"])
@jwt_required()
def new_reservation(book_id):
    book = Book.query.get(book_id)
    if not book:
        return {"error": "Book id not found."}, 404
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return {"error": "User not found in the database"}, 403
    reservation = Reservation(
        date = date.today(),
        book = book,
        user = user,
    )
    db.session.add(reservation)
    db.session.commit()
    return jsonify(reservation_schema.dump(reservation)), 200