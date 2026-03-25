"""Book models."""

from .library_resource import LibraryResource


class Book(LibraryResource):
    """Represents a physical book."""

    def __init__(self, resource_id, title, author, year):
        super().__init__(resource_id, title)
        self.author = author
        self.year = year

    def get_info(self):
        return f"{self.title} by {self.author.name} ({self.year})"


class EBook(Book):
    """Represents a digital book."""

    def __init__(self, resource_id, title, author, year, file_size):
        super().__init__(resource_id, title, author, year)
        self.file_size = file_size

    def get_info(self):
        return f"EBook: {self.title} by {self.author.name} ({self.year}) - {self.file_size}MB"


class AudioBook(Book):
    """Represents an audiobook."""

    def __init__(self, resource_id, title, author, year, duration):
        super().__init__(resource_id, title, author, year)
        self.duration = duration

    def get_info(self):
        return f"Audiobook: {self.title} by {self.author.name} ({self.year}) - {self.duration} mins"