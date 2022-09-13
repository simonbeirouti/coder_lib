from main import ma 
from marshmallow import fields
from schemas.user_schema import UserSchema
from schemas.book_schema import BookSchema

class ReservationSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("reservation_id", "user", "book", "date", "length", "book_id", "user_id", "librarian_id", "reservation")
        load_only = ["book_id", "user_id", "librarian_id"]
    user = fields.Nested(UserSchema, only=("username", "email"))
    book = fields.Nested(BookSchema, only=("title", "genre"))

reservation_schema = ReservationSchema()
reservations_schema = ReservationSchema(many=True)