from main import ma

class LibrarianSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("librarian_id", "username", "email", "password", "name", "shift")

librarian_schema = LibrarianSchema()