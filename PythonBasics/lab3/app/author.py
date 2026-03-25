"""Author model."""


class Author:
    """Represents a book author."""

    def __init__(self, name, nationality):
        self.name = name
        self.nationality = nationality

    def __repr__(self):
        return f"Author(name='{self.name}', nationality='{self.nationality}')"

    def __eq__(self, other):
        if isinstance(other, Author):
            return self.name == other.name
        return False