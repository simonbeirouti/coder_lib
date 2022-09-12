from datetime import timedelta
from flask import Blueprint, jsonify, request
from main import db, bcrypt
from flask_jwt_extended import create_access_token
from models.users import User
from schemas.user_schema import user_schema

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
        return {"error": "User not found."}, 404
    if user.password != user_fields["password"]:
        return {"error": "Wrong password."}, 404
    return jsonify(user_schema.dump(user))

@auth.route("/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return {"error": "User id not found."}, 404
    db.session.delete(user)
    db.session.commit()
    return jsonify(user_schema.dump(user))

@auth.route("/<int:id>", methods=["PUT"])
def update_user(id):
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