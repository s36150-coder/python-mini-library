"""
Book model for the Mini Library system.
"""


class Book:
    """Represents a single book in the library."""

    def __init__(self, book_id: int, title: str, author: str, year: int, genre: str):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre
        self.is_available = True

    def to_dict(self) -> dict:
        """Convert book to a dictionary (used for JSON serialization)."""
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "genre": self.genre,
            "is_available": self.is_available,
        }

    @staticmethod
    def from_dict(data: dict) -> "Book":
        """Create a Book instance from a dictionary (used when loading from JSON)."""
        book = Book(
            book_id=data["book_id"],
            title=data["title"],
            author=data["author"],
            year=data["year"],
            genre=data["genre"],
        )
        book.is_available = data.get("is_available", True)
        return book

    def __str__(self) -> str:
        status = "Available" if self.is_available else "Borrowed"
        return f"[{self.book_id}] '{self.title}' by {self.author} ({self.year}) | {self.genre} | {status}"
