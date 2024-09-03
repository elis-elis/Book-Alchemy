from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
# it initializes an instance of the SQLAlchemy class, which provides various database-related functionalities,
# including the column types and methods necessary for defining models.


class Author(db.Model):
    __tablename__ = 'authors'

    author_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=True)
    date_of_death = db.Column(db.Date, nullable=True)

    # Optional: customize the string representation of the Author instance
    def __repr__(self):
        return f"<Author(id={self.author_id}, name='{self.author_name}')>"

    def __str__(self):
        return f"{self.author_name} (Born: {self.birth_date}, Died: {self.date_of_death})"


class Book(db.Model):
    __tablename__ = 'books'

    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String(13), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.author_id'), nullable=False)
    # This creates a link between the two tables,
    # establishing a "many-to-one" relationship (many books can be written by one author).

    def __repr__(self):
        return f"<Book(id={self.book_id}, title='{self.book_title}', isbn='{self.isbn}')>"

    def __str__(self):
        return f"'{self.title}' by {self.author.author_name}, (ISBN: {self.isbn}, Published: {self.publication_year})"
