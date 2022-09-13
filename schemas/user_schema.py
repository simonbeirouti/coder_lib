from main import ma 
from marshmallow.validate import Length
import re

regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

def isValid(email):
    if re.fullmatch(regex, email):
      return True
    else:
      return False

class UserSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("user_id", "username", "email", "password")
    password = ma.String(validate=Length(min=8))
    username = ma.String(validate=Length(min=5), required = True)
    email = ma.String(validate=isValid, required = True)

user_schema = UserSchema()