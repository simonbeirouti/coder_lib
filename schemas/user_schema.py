from main import ma 
from marshmallow.validate import Length

class UserSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("user_id", "username", "email", "password", "admin")
    password = ma.String(validate=Length(min=8))

user_schema = UserSchema()