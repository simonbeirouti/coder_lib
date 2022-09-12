from main import ma

class AuthorSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("author_id", "first_name", "last_name", "country", "dob")

author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)