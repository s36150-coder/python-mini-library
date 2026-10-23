"""
Custom exceptions for the Mini Library system.

Having your own exception classes makes error handling specific and clear.
Instead of catching a generic Exception, we catch exactly what went wrong.
"""


class LibraryError(Exception):
    """Base exception for all library-related errors."""
    pass


class BookNotFoundError(LibraryError):
    """Raised when a book with the given ID does not exist."""
    def __init__(self, book_id: int):
        super().__init__(f"Book with ID {book_id} was not found in the library.")
        self.book_id = book_id


class UserNotFoundError(LibraryError):
    """Raised when a user with the given ID does not exist."""
    def __init__(self, user_id: int):
        super().__init__(f"User with ID {user_id} does not exist.")
        self.user_id = user_id


class BookNotAvailableError(LibraryError):
    """Raised when a user tries to borrow a book that is already borrowed."""
    def __init__(self, book_id: int):
        super().__init__(f"Book {book_id} is currently not available (already borrowed).")
        self.book_id = book_id


class InvalidEmailError(LibraryError):
    """Raised when a user provides an email address that fails regex validation."""
    def __init__(self, email: str):
        super().__init__(f"'{email}' is not a valid email address.")
        self.email = email
