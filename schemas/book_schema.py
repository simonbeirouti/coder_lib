from main import ma
from marshmallow import fields
from schemas.author_schema import AuthorSchema

class BookSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("book_id", "title", "genre", "year", "length", "author_id", "author")
        load_only = ['author_id', 'book_id']
    author = fields.Nested(AuthorSchema, only=("name", "country", "dob"))

book_schema = BookSchema()
books_schema = BookSchema(many=True)