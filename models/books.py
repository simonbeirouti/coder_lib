from main import db

class Book(db.Model):
    __tablename__ = 'books'
    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    genre = db.Column(db.String(), nullable=False)
    year = db.Column(db.Date(), nullable=False)
    length = db.Column(db.Integer, nullable=False)
    # author_id = db.Column(db.Integer, db.ForeignKey('authors.author_id'), nullable=False)