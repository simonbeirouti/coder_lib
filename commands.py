from flask import Blueprint
from main import db
from main import bcrypt
from models.authors import Author
from models.books import Book
from models.users import User
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
        ['J. D.', 'Salinger', 'United States of America', 1, 1, 1919],
        ['J. R. R.', 'Tolkien', 'United Kingdom', 3, 1, 1892]]
    books = [
        ['The Grapes of Wrath', 'Fiction', 464, 14, 4, 1939], 
        ['The Great Gatsby', 'Fiction', 180, 10, 4, 1925], 
        ['Harry Potter and the Philosopher\'s Stone', 'Fantasy', 352, 26, 6, 1997], 
        ['Harry Potter and the Chamber of Secrets', 'Fantasy', 251, 2, 7, 1998], 
        ['Harry Potter and the Prisoner of Azkaban', 'Fantasy', 317, 8, 7, 1999], 
        ['Harry Potter and the Goblet of Fire', 'Fantasy', 636, 8, 7, 2000], 
        ['Harry Potter and the Order of the Phoenix', 'Fantasy', 766, 21, 6, 2003], 
        ['Harry Potter and the Half-Blood Prince', 'Fantasy', 607, 16, 7, 2005], 
        ['Harry Potter and the Deathly Hallows', 'Fantasy', 607, 21, 7, 2007], 
        ['LOTR: The Fellowship of the Ring', 'Fantasy', 423, 29, 7, 1954],
        ['LOTR: The Two Towers', 'Fantasy', 352, 11, 11, 1954],
        ['LOTR: The Return of the King', 'Fantasy', 416, 1, 2, 1955],
        ['It', 'Horror', 1138, 15, 8, 1986], 
        ['1984', 'Fiction', 304, 8, 6, 1949], 
        ['To Kill a Mockingbird', 'Fiction', 384, 11, 7, 1960], 
        ['The Catcher in the Rye', 'Fiction', 240, 16, 7, 1951]]
    users = [
        ['simonbe', 'hi@e.com', '123qwe123', True],
        ['simonbe2', 'bye@e.com', '123qwe123', False],
        ['user1', '1@e.com', '123qwe123', False],
        ['user2', '2@e.com', '123qwe123', False]]
    for author in authors:
        new_author = Author(
            first_name = author[0], 
            last_name = author[1], 
            country = author[2], 
            dob = date(day = author[3], month = author[4], year = author[5])
        )
        db.session.add(new_author)
    for book in books:
        new_book = Book(
            title = book[0], 
            genre = book[1], 
            length = book[2], 
            year = date(day = book[3], month = book[4], year = book[5])
        )
        db.session.add(new_book)
    for user in users:
        new_user = User(
            username = user[0], 
            email = user[1], 
            password = bcrypt.generate_password_hash(user[2]).decode('utf-8'),
            admin = user[3]
        )
        db.session.add(new_user)
    db.session.commit()
    print("Database seeded.")
    