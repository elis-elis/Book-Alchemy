from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
import os
from data_models import db, Author, Book
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'
db_path = os.path.join(os.getcwd(), 'data', 'library.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/library.sqlite'

db.init_app(app)
# This will connect the Flask app to the flask-sqlalchemy code
# now has access to the database

# with app.app_context():
#     db.create_all()


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        # Get data from the form
        author_name = request.form.get('author_name')
        birth_date_str = request.form.get('birth_date')
        date_of_death_str = request.form.get('date_of_death')

        # Convert the birthdate, if provided
        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date() \
            if birth_date_str else None
        # Convert the date of death, if provided
        date_of_death = datetime.strptime(date_of_death_str, '%Y-%m-%d').date() \
            if date_of_death_str else None

        # Validate and add the new author to the database
        if author_name:
            # Creates a new instance of the Author model using the data provided in the form
            new_author = Author(author_name=author_name, birth_date=birth_date, date_of_death=date_of_death)
            db.session.add(new_author)
            db.session.commit()
            flash('Author added successfully! 🌈', 'success')
            return redirect(url_for('add_author'))
            # important to avoid re-submission of the form if the user refreshes the page after submitting
        else:
            flash('Author name is a requirement! 🌊', 'error')

    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        # Retrieve data from form
        title = request.form.get('title')
        isbn = request.form.get('isbn')
        publication_year = request.form.get('publication_year')
        author_id = request.form.get('author_id')

        # Validate the required fields
        if title and isbn and author_id:
            new_book = Book(title=title, isbn=isbn, publication_year=publication_year, author_id=author_id)
            db.session.add(new_book)
            db.session.commit()
            flash('Book added successfully! 🪭', 'success')
            return redirect(url_for('add_book'))
        else:
            flash('All fields are required here! ⚡️', 'error')

    # Handle GET request to display the form
    authors = Author.query.all()
    return render_template('add_book.html', authors=authors)
    # Passes the list of authors to the template so that the dropdown menu can be
    # dynamically populated with existing authors from the database


@app.route('/')
def home_page():
    # Get sorting parameter from the request
    sort_by = request.args.get('sort_by', 'title')  # Default to 'title'

    # Define the sorting logic based on the parameter
    if sort_by == 'author':
        books = db.session.query(Book, Author).join(Author).order_by(Author.author_name).all()
    elif sort_by == 'publication_year':
        books = db.session.query(Book, Author).join(Author).order_by(Book.publication_year).all()
    else:
        books = db.session.query(Book, Author).join(Author).order_by(Book.title).all()

    book_data = []

    # iterates over the results of the query (books), which are tuples of (book, author)
    for book, author in books:
        book_data.append({
            'title': book.title,
            'author_name': author.author_name,
            'isbn': book.isbn,
            'publication_year': book.publication_year,
            'cover_image_url': get_cover_image(book.isbn)
        })

    # Render the home.html template with the books data
    return render_template('home_page.html', books=book_data, sort_by=sort_by)


def get_cover_image(isbn):
    # Use the Open Library Covers API to get the cover image URL
    cover_url = f"http://covers.openlibrary.org/b/isbn/{isbn}-M.jpg"

    # Check if the image exists by making a request
    response = requests.get(cover_url)

    # If the image exists, return the URL, otherwise return a placeholder image
    if response.status_code == 200:
        return cover_url
    else:
        return '/static/images/placeholder.jpg'  # Placeholder image in case cover is not available


if __name__ == '__main__':
    app.run(debug=True)
