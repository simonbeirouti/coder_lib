from flask import Blueprint
from main import db
from main import bcrypt
from models.authors import Author
from models.books import Book
from models.users import User
from models.librarians import Librarian
from models.reservation import Reservation
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
        ['John Steinbeck', 'United States of America', 27, 2, 1902], 
        ['F. Scott Fitzgerald', 'United States of America', 24, 9, 1896], 
        ['J.K. Rowling', 'United Kingdom', 31, 7, 1965], 
        ['Stephen King', 'United States of America', 21, 9, 1947],
        ['George Orwell', 'Indian', 25, 6, 1903],
        ['Harper Lee', 'United States of America', 28, 4, 1926], 
        ['J. D. Salinger', 'United States of America', 1, 1, 1919],
        ['J. R. R. Tolkien', 'United Kingdom', 3, 1, 1892]]
    books = [
        ['The Grapes of Wrath', 'Fiction', 464, 14, 4, 1939, 1], 
        ['The Great Gatsby', 'Fiction', 180, 10, 4, 1925, 2], 
        ['Harry Potter and the Philosopher\'s Stone', 'Fantasy', 352, 26, 6, 1997, 3], 
        ['Harry Potter and the Chamber of Secrets', 'Fantasy', 251, 2, 7, 1998, 3], 
        ['Harry Potter and the Prisoner of Azkaban', 'Fantasy', 317, 8, 7, 1999, 3], 
        ['Harry Potter and the Goblet of Fire', 'Fantasy', 636, 8, 7, 2000, 3], 
        ['Harry Potter and the Order of the Phoenix', 'Fantasy', 766, 21, 6, 2003, 3], 
        ['Harry Potter and the Half-Blood Prince', 'Fantasy', 607, 16, 7, 2005, 3], 
        ['Harry Potter and the Deathly Hallows', 'Fantasy', 607, 21, 7, 2007, 3], 
        ['LOTR: The Fellowship of the Ring', 'Fantasy', 423, 29, 7, 1954, 8],
        ['LOTR: The Two Towers', 'Fantasy', 352, 11, 11, 1954, 8],
        ['LOTR: The Return of the King', 'Fantasy', 416, 1, 2, 1955, 8],
        ['It', 'Horror', 1138, 15, 8, 1986, 4], 
        ['1984', 'Fiction', 304, 8, 6, 1949, 5], 
        ['To Kill a Mockingbird', 'Fiction', 384, 11, 7, 1960, 6], 
        ['The Catcher in the Rye', 'Fiction', 240, 16, 7, 1951, 7]]
    users = [
        ['simonbe', 'hi@e.com', '123qwe123'],
        ['simonbe2', 'bye@e.com', '123qwe123'],
        ['user1', '1@e.com', '123qwe123'],
        ['user2', '2@e.com', '123qwe123']]
    librarians = [
        ['StacyWo', 'sc@lib.com', '123qwe123', 'Stacy Wo'],
        ['RegalBro', 'rb@lib.com', '123qwe123', 'Regal Bro'],
        ['TuPac', 'tp@lib.com', '123qwe123', 'Tu Pac']]
    reservations = [
        [date.today(), 5, 1, 1, 1],
        [date.today(), 5, 2, 1, 1],
        [date.today(), 5, 4, 1, 1],
        [date.today(), 10, 3, 2, 1],
        [date.today(), 10, 5, 3, 1],
        [date.today(), 7, 6, 2, 1]]
    for author in authors:
        new_author = Author(
            name = author[0],
            country = author[1], 
            dob = date(day = author[2], month = author[3], year = author[4])
        )
        db.session.add(new_author)
    db.session.commit()
    for book in books:
        new_book = Book(
            title = book[0], 
            genre = book[1], 
            length = book[2], 
            year = date(day = book[3], month = book[4], year = book[5]),
            author_id = book[6]
        )
        db.session.add(new_book)
    db.session.commit()
    for user in users:
        new_user = User(
            username = user[0], 
            email = user[1], 
            password = bcrypt.generate_password_hash(user[2]).decode('utf-8')
        )
        db.session.add(new_user)
    db.session.commit()
    for librarian in librarians:
        new_librarian = Librarian(
            username = librarian[0], 
            email = librarian[1], 
            password = bcrypt.generate_password_hash(librarian[2]).decode('utf-8'),
            name = librarian[3]
        )
        db.session.add(new_librarian)
    db.session.commit()
    for reservation in reservations:
        new_reservation = Reservation(
            date = reservation[0],
            length = reservation[1],
            book_id = reservation[2],
            user_id = reservation[3],
            librarian_id = reservation[4]
        )
        db.session.add(new_reservation)
    db.session.commit()
    print("Database seeded.")
    