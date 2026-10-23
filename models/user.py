"""
User model for the Mini Library system.
"""


class User:
    """Represents a registered library member."""

    def __init__(self, user_id: int, name: str, email: str):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.borrowed_book_ids: list[int] = []

    def to_dict(self) -> dict:
        """Convert user to a dictionary (used for JSON serialization)."""
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "borrowed_book_ids": self.borrowed_book_ids,
        }

    @staticmethod
    def from_dict(data: dict) -> "User":
        """Create a User instance from a dictionary (used when loading from JSON)."""
        user = User(
            user_id=data["user_id"],
            name=data["name"],
            email=data["email"],
        )
        user.borrowed_book_ids = data.get("borrowed_book_ids", [])
        return user

    def __str__(self) -> str:
        return f"[{self.user_id}] {self.name} <{self.email}> | Borrowed: {len(self.borrowed_book_ids)} book(s)"
