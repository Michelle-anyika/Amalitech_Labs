"""Main program for Library Inventory."""

from app.book import Book
from app.author import Author
from app.inventory import Inventory


def main():
    inventory = Inventory()

    author = Author("George Orwell", "British")

    book1 = Book(1, "1984", author, 1949)
    book2 = Book(2, "Animal Farm", author, 1945)

    inventory.add_resource(book1)
    inventory.add_resource(book2)

    print("\nLibrary Inventory:")
    for book in inventory.list_resources():
        print(book.get_info())

    print("\nSearch result for '1984':")
    results = inventory.search_by_title("1984")
    for r in results:
        print(r.get_info())

    inventory.save_to_file()


if __name__ == "__main__":
    main()