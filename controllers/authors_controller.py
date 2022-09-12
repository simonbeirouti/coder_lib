from flask import Blueprint, jsonify, request
from main import db
from models.authors import Author
from schemas.author_schema import author_schema, authors_schema

authors = Blueprint("authors", __name__, url_prefix="/authors")

@authors.route("/", methods=["GET"])
def get_authors():
    authors_list = Author.query.all()
    result = authors_schema.dump(authors_list)
    return jsonify(result)

@authors.route("/<int:id>", methods=["GET"])
def get_author(id):
    author = Author.query.get(id)
    if not author:
        return {"error": "Author id not found."}, 404
    result = author_schema.dump(author)
    return jsonify(result)

@authors.route("/", methods=["POST"])
def new_author():
    author_fields = author_schema.load(request.json)
    author = Author(
        first_name = author_fields["first_name"],
        last_name = author_fields["last_name"],
        country = author_fields["country"],
        dob = author_fields["dob"],
    )
    db.session.add(author)
    db.session.commit()
    return jsonify(author_schema.dump(author))

@authors.route("/<int:id>", methods=["DELETE"])
def delete_author(id):
    author = Author.query.get(id)
    if not author:
        return {"error": "Author id not found."}, 404
    db.session.delete(author)
    db.session.commit()
    return jsonify(author_schema.dump(author))

@authors.route("/<int:id>", methods=["PUT"])
def update_author(id):
    author = Author.query.get(id)
    if not author:
        return {"error": "Author id not found."}, 404
    author_fields = author_schema.load(request.json)
    author.first_name = author_fields["first_name"]
    author.last_name = author_fields["last_name"]
    author.country = author_fields["country"]
    author.dob = author_fields["dob"]
    db.session.commit()
    return jsonify(author_schema.dump(author))