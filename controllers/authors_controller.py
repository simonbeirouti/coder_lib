from flask import Blueprint, jsonify
from main import db
from models.authors import Author
from schemas.author_schema import author_schema, authors_schema

authors = Blueprint("authors", __name__, url_prefix="/authors")

@authors.route("/", methods=["GET"])
def get_authors():
    authors_list = Author.query.all()
    result = authors_schema.dump(authors_list)
    return result

@authors.route("/<int:id>", methods=["GET"])
def get_author(id):
    author = Author.query.get(id)
    result = author_schema.dump(author)
    return result