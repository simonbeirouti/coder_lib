from main import ma
from marshmallow import fields

class AuthorSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("author_id", "name", "country", "dob", "books")
        load_only = ["author_id"]
    books = fields.List(fields.Nested("BookSchema", only=("title", "genre", "year", "length")))

author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)