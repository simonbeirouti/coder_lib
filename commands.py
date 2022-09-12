from flask import Blueprint
from main import db
from models.authors import Author
from models.books import Book
from datetime import date

db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_db():
    db.create_all()
    print("Database created.")

@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    print("Database dropped.")

@db_commands.cli.command("seed")
def seed_db():
    authors = [
        ['John', 'Steinbeck', 'United States of America', 27, 2, 1902], 
        ['F. Scott', 'Fitzgerald', 'United States of America', 24, 9, 1896], 
        ['J.K.', 'Rowling', 'United Kingdom', 31, 7, 1965], 
        ['Stephen', 'King', 'United States of America', 21, 9, 1947],
        ['George', 'Orwell', 'Indian', 25, 6, 1903],
        ['Harper', 'Lee', 'United States of America', 28, 4, 1926], 
        ['J. D.', 'Salinger', 'United States of America', 1, 1, 1919]]
    books = [
        ['The Grapes of Wrath', 'Fiction', 464, 14, 4, 1939], 
        ['The Great Gatsby', 'Fiction', 180, 10, 4, 1925], 
        ['Harry Potter and the Philosopher\'s Stone', 'Fantasy', 352, 26, 6, 1997], 
        ['It', 'Horror', 1138, 15, 8, 1986], 
        ['1984', 'Fiction', 304, 8, 6, 1949], 
        ['To Kill a Mockingbird', 'Fiction', 384, 11, 7, 1960], 
        ['The Catcher in the Rye', 'Fiction', 240, 16, 7, 1951]]
    for author in authors:
        new_author = Author(
            first_name=author[0], 
            last_name=author[1], 
            country=author[2], 
            dob=date(day = author[3], month = author[4], year = author[5])
        )
        db.session.add(new_author)
    for book in books:
        new_book = Book(
            title=book[0], 
            genre=book[1], 
            length=book[2], 
            year=date(day = book[3], month = book[4], year = book[5])
        )
        db.session.add(new_book)

    db.session.commit()
    print("Database seeded.")
    