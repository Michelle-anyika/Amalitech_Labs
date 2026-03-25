from app.book import Book
from app.author import Author


def test_book_creation():
    author = Author("Test Author", "Test Country")
    book = Book(1, "Test Book", author, 2024)

    assert book.title == "Test Book"
    assert book.author.name == "Test Author"