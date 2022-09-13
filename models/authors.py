from main import db

class Author(db.Model):
    __tablename__ = 'authors'
    author_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    country = db.Column(db.String(), nullable=False)
    dob = db.Column(db.Date(), nullable=False)
    books = db.relationship('Book', backref='author')