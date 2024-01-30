from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(64), nullable=True)
    occupation = db.Column(db.String(64), nullable=True)
    def check_password(self, password):
        return self.password == password

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(64), nullable=False)
    date_issue = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('sections.id'), nullable=False)
    borrowers = db.relationship('Borrowing', backref='book', lazy=True)
    issued_books = db.relationship('Issued', backref='book', lazy=True)
class Section(db.Model):
    __tablename__ = 'sections'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    date_created = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(120), nullable=False)

    
class Borrowing(db.Model):
    __tablename__ = 'borrowings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)

class Issued(db.Model):
    __tablename__ = 'issued'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
