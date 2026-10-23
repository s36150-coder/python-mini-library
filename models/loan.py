"""
Loan model — tracks which user borrowed which book and when.
"""
from datetime import date


class Loan:
    """Represents a single borrowing event."""

    def __init__(self, loan_id: int, user_id: int, book_id: int, loan_date: str = None):
        self.loan_id = loan_id
        self.user_id = user_id
        self.book_id = book_id
        self.loan_date = loan_date or date.today().isoformat()
        self.return_date: str | None = None

    def is_active(self) -> bool:
        """Return True if the book has not been returned yet."""
        return self.return_date is None

    def to_dict(self) -> dict:
        return {
            "loan_id": self.loan_id,
            "user_id": self.user_id,
            "book_id": self.book_id,
            "loan_date": self.loan_date,
            "return_date": self.return_date,
        }

    @staticmethod
    def from_dict(data: dict) -> "Loan":
        loan = Loan(
            loan_id=data["loan_id"],
            user_id=data["user_id"],
            book_id=data["book_id"],
            loan_date=data["loan_date"],
        )
        loan.return_date = data.get("return_date")
        return loan

    def __str__(self) -> str:
        status = "ACTIVE" if self.is_active() else f"Returned: {self.return_date}"
        return (
            f"Loan #{self.loan_id} | User {self.user_id} → Book {self.book_id} "
            f"| Borrowed: {self.loan_date} | {status}"
        )
