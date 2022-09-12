from main import ma

class BookSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("book_id", "title", "genre", "year", "length")

book_schema = BookSchema()
books_schema = BookSchema(many=True)