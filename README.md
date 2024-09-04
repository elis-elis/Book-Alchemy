## °°°°°° E's Library Management System °°°°°°°
![screenshot.png](screenshot.png)

This web application allows users to manage a collection of books and authors, including adding new entries, viewing existing ones, and deleting entries when needed.

**Features:**

* Add New Authors: Create and save new authors with their name, birthdate, and date of death.
* Add New Books: Create and save new books with title, ISBN, publication year, and assign an author.
* Search and Sort: Search books by title or author and sort results by title, author name, or publication year.
* Delete Books: Remove books from the collection; if the deleted book was the last one by an author, the author is also deleted.

**Project Structure:**

* app.py: Main application file containing all routes and logic.
* data_models.py: Defines the data models for Authors and Books.
* templates/: Contains HTML files for rendering web pages.
* static/: Contains static files like CSS styles and images.

**Prerequisites:**

Install Flask using pip

Install SQLAlchemy using pip

Install the Requests library for fetching book covers
