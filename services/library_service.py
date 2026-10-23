"""
Library service — the main business logic of the Mini Library.

This file contains:
  - Collections (lists, dicts, sets)
  - Comprehensions (list / dict / set)
  - Generator function
  - Lambda functions
  - Control statements (if, for, while)
  - Operators (arithmetic, logical, comparison)
  - The @log_action decorator applied to key methods
  - Custom exception handling
"""
from datetime import date

from models.book import Book
from models.loan import Loan
from models.user import User
from services.file_service import load_json, save_json
from utils.decorators import log_action
from utils.exceptions import (
    BookNotAvailableError,
    BookNotFoundError,
    UserNotFoundError,
)

DATA_FILE = "data/library.json"


class LibraryService:
    """Central service that manages books, users, and loans."""

    def __init__(self):
        # --- Collections: three dictionaries used as the in-memory database ---
        self.books: dict[int, Book] = {}
        self.users: dict[int, User] = {}
        self.loans: dict[int, Loan] = {}
        self._load()

    # ------------------------------------------------------------------ #
    #  Persistence                                                         #
    # ------------------------------------------------------------------ #

    def _load(self) -> None:
        """Load all data from the JSON file into memory."""
        data = load_json(DATA_FILE)
        self.books = {b["book_id"]: Book.from_dict(b) for b in data["books"]}
        self.users = {u["user_id"]: User.from_dict(u) for u in data["users"]}
        self.loans = {l["loan_id"]: Loan.from_dict(l) for l in data["loans"]}

    def _save(self) -> None:
        """Persist the current in-memory state to the JSON file."""
        data = {
            "books": [b.to_dict() for b in self.books.values()],
            "users": [u.to_dict() for u in self.users.values()],
            "loans": [l.to_dict() for l in self.loans.values()],
        }
        save_json(DATA_FILE, data)

    # ------------------------------------------------------------------ #
    #  Helper: ID generation                                               #
    # ------------------------------------------------------------------ #

    def _next_id(self, collection: dict) -> int:
        """Return the next available integer ID for a collection."""
        # Arithmetic operator: max(...) + 1
        return max(collection.keys(), default=0) + 1

    # ------------------------------------------------------------------ #
    #  Books                                                               #
    # ------------------------------------------------------------------ #

    @log_action
    def add_book(self, title: str, author: str, year: int, genre: str) -> Book:
        """Add a new book to the library."""
        book_id = self._next_id(self.books)
        book = Book(book_id, title, author, year, genre)
        self.books[book_id] = book
        self._save()
        print(f"  Book added: {book}")
        return book

    def get_book(self, book_id: int) -> Book:
        """Retrieve a book by ID, raising BookNotFoundError if missing."""
        if book_id not in self.books:
            raise BookNotFoundError(book_id)
        return self.books[book_id]

    def list_books(self) -> list[Book]:
        """Return all books sorted by title (using a lambda as the sort key)."""
        # Lambda: used as sort key — sorts books alphabetically by title
        return sorted(self.books.values(), key=lambda b: b.title.lower())

    def search_books(self, query: str) -> list[Book]:
        """
        Search books by title or author (case-insensitive).

        Uses a LIST COMPREHENSION to filter books in one readable line.
        """
        q = query.lower()
        # List comprehension: [ item for item in iterable if condition ]
        return [
            book for book in self.books.values()
            if q in book.title.lower() or q in book.author.lower()
        ]

    def available_books(self) -> list[Book]:
        """Return only books that are currently available for borrowing."""
        # Another list comprehension — filters by the is_available flag
        return [book for book in self.books.values() if book.is_available]

    def genres_summary(self) -> dict[str, int]:
        """
        Return a dictionary mapping each genre to the number of books in it.

        Uses a DICT COMPREHENSION to build the result.
        """
        # First collect unique genres with a SET COMPREHENSION
        genres: set[str] = {book.genre for book in self.books.values()}

        # Then build a dict: { genre: count } using a dict comprehension
        return {
            genre: sum(1 for b in self.books.values() if b.genre == genre)
            for genre in genres
        }

    # ------------------------------------------------------------------ #
    #  Users                                                               #
    # ------------------------------------------------------------------ #

    @log_action
    def add_user(self, name: str, email: str) -> User:
        """Register a new library member."""
        user_id = self._next_id(self.users)
        user = User(user_id, name, email)
        self.users[user_id] = user
        self._save()
        print(f"  User registered: {user}")
        return user

    def get_user(self, user_id: int) -> User:
        if user_id not in self.users:
            raise UserNotFoundError(user_id)
        return self.users[user_id]

    def list_users(self) -> list[User]:
        """Return all users sorted by name."""
        return sorted(self.users.values(), key=lambda u: u.name.lower())

    # ------------------------------------------------------------------ #
    #  Loans                                                               #
    # ------------------------------------------------------------------ #

    @log_action
    def borrow_book(self, user_id: int, book_id: int) -> Loan:
        """
        Lend a book to a user.

        Raises:
            UserNotFoundError  — if the user does not exist
            BookNotFoundError  — if the book does not exist
            BookNotAvailableError — if the book is already borrowed
        """
        user = self.get_user(user_id)   # raises UserNotFoundError if needed
        book = self.get_book(book_id)   # raises BookNotFoundError if needed

        # Logical + comparison operators
        if not book.is_available:
            raise BookNotAvailableError(book_id)

        loan_id = self._next_id(self.loans)
        loan = Loan(loan_id, user_id, book_id)

        book.is_available = False
        user.borrowed_book_ids.append(book_id)
        self.loans[loan_id] = loan

        self._save()
        print(f"  Loan created: {loan}")
        return loan

    @log_action
    def return_book(self, user_id: int, book_id: int) -> Loan:
        """
        Process a book return.

        Finds the active loan for the given user+book pair and closes it.
        """
        user = self.get_user(user_id)
        book = self.get_book(book_id)

        # Find the active loan using next() with a generator expression.
        # Generator expression: (item for item in iterable if condition)
        # next(..., None) returns the first match or None if there is none.
        active_loan = next(
            (
                loan for loan in self.loans.values()
                if loan.user_id == user_id
                and loan.book_id == book_id
                and loan.is_active()
            ),
            None,
        )

        if active_loan is None:
            raise BookNotFoundError(book_id)

        active_loan.return_date = date.today().isoformat()
        book.is_available = True

        # Remove from user's list using list comprehension (rebuild without book_id)
        user.borrowed_book_ids = [
            bid for bid in user.borrowed_book_ids if bid != book_id
        ]

        self._save()
        print(f"  Book returned: {book.title}")
        return active_loan

    def active_loans(self) -> list[Loan]:
        """Return all loans that have not been returned yet."""
        # List comprehension + method call (is_active)
        return [loan for loan in self.loans.values() if loan.is_active()]

    # ------------------------------------------------------------------ #
    #  Generator function                                                  #
    # ------------------------------------------------------------------ #

    def overdue_warnings(self, max_days: int = 30):
        """
        GENERATOR FUNCTION — yields warning strings for long-running loans.

        A generator uses 'yield' instead of 'return'.
        It produces values one at a time, without building a full list in memory.
        This is useful when dealing with potentially large datasets.
        """
        today = date.today()
        for loan in self.loans.values():
            if loan.is_active():
                loan_date = date.fromisoformat(loan.loan_date)
                # Arithmetic operator: subtraction of two date objects
                days_borrowed = (today - loan_date).days
                if days_borrowed > max_days:
                    user = self.users.get(loan.user_id)
                    book = self.books.get(loan.book_id)
                    user_name = user.name if user else f"User#{loan.user_id}"
                    book_title = book.title if book else f"Book#{loan.book_id}"
                    # 'yield' — this is what makes the function a generator
                    yield f"  WARNING: '{book_title}' borrowed by {user_name} for {days_borrowed} days!"
