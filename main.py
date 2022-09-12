from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.app_config')
    
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    from commands import db_commands
    app.register_blueprint(db_commands)

    from controllers import registerable_controllers
    for i in registerable_controllers:
        app.register_blueprint(i)

    return app
