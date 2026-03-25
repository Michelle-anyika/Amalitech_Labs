"""Borrowing logic."""


class Borrow:
    """Represents a borrowed resource."""

    def __init__(self, borrower_name, resource):
        self.borrower_name = borrower_name
        self.resource = resource
        self.returned = False

    def mark_returned(self):
        """Mark resource as returned."""
        self.returned = True

    def __repr__(self):
        status = "Returned" if self.returned else "Borrowed"
        return f"{self.borrower_name} -> {self.resource.title} ({status})"