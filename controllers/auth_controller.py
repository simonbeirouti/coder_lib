from datetime import timedelta
from flask import Blueprint, jsonify, request
from main import db, bcrypt
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from models.users import User
from schemas.user_schema import user_schema
from models.librarians import Librarian
from schemas.librarian_schema import librarian_schema

auth = Blueprint("auth", __name__, url_prefix="/auth")

@auth.route("/register", methods=["POST"])
def register_user():
    user_fields = user_schema.load(request.json)
    user = User.query.filter_by(username=user_fields["username"]).first()
    if user:
        return {"error": "User already exists."}, 400
    user = User.query.filter_by(email=user_fields["email"]).first()
    if user:
        return {"error": "Email already exists."}, 400
    user = User(
        username = user_fields["username"],
        password = bcrypt.generate_password_hash(user_fields["password"]).decode("utf-8"),
        email = user_fields["email"],
        admin = user_fields["admin"],
    )
    db.session.add(user)
    db.session.commit()
    token = create_access_token(identity=str(user.user_id), expires_delta=timedelta(days=1))
    return {"username": user.username, "token": token}

@auth.route("/login", methods=["POST"])
def login_user():
    user_fields = user_schema.load(request.json)
    user = User.query.filter_by(username=user_fields["username"]).first()
    if not user:
        return {"error": "Username is not valid."}, 404
    if not bcrypt.check_password_hash(user.password, user_fields["password"]):
        return {"error": "Password is not valid."}, 404
    token = create_access_token(identity=str(user.user_id), expires_delta=timedelta(days=1))
    return {"username": user.username, "token": token}

@auth.route("/librarian/login", methods=["POST"])
def login_librarian():
    librarian_fields = librarian_schema.load(request.json)
    librarian = Librarian.query.filter_by(username=librarian_fields["username"]).first()
    if not librarian:
        return {"error": "Username is not valid."}, 404
    if not bcrypt.check_password_hash(librarian.password, librarian_fields["password"]):
        return {"error": "Password is not valid."}, 404
    token = create_access_token(identity="librarian", expires_delta=timedelta(days=1))
    return {"librarian": librarian.username, "token": token}

@auth.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_user(id):
    if get_jwt_identity() != "librarian":
        return {"error": "Only librarians can delete users."}, 403
    user = User.query.get(id)
    if not user:
        return {"error": "User id not found."}, 404
    db.session.delete(user)
    db.session.commit()
    return jsonify(user_schema.dump(user))

@auth.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_user(id):
    if get_jwt_identity() != "librarian":
        return {"error": "Only librarians can update users."}, 403
    user = User.query.get(id)
    if not user:
        return {"error": "User id not found."}, 404
    user_fields = user_schema.load(request.json)
    user.username = user_fields["username"]
    user.password = user_fields["password"]
    user.email = user_fields["email"]
    user.dob = user_fields["dob"]
    db.session.commit()
    return jsonify(user_schema.dump(user))