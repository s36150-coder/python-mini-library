"""
main.py — entry point for the Mini Library application.

Run this file to start the program:
    python main.py
"""
from services.library_service import LibraryService
from utils.exceptions import LibraryError
from utils.validators import validate_email, validate_non_empty, validate_year


def print_header(title: str) -> None:
    """Print a simple section header."""
    print(f"\n{'=' * 50}")
    print(f"  {title}")
    print('=' * 50)


def get_int(prompt: str) -> int:
    """Ask the user for an integer, repeating until they enter a valid one."""
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("  Please enter a valid number.")


def menu_books(service: LibraryService) -> None:
    """Sub-menu for book management."""
    while True:
        print_header("BOOKS")
        print("  1. List all books")
        print("  2. Search books")
        print("  3. Add a book")
        print("  4. Available books")
        print("  5. Genres summary")
        print("  0. Back")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            books = service.list_books()
            if not books:
                print("  No books in the library yet.")
            for book in books:
                print(" ", book)

        elif choice == "2":
            query = input("  Search (title or author): ").strip()
            results = service.search_books(query)
            if not results:
                print("  No books found.")
            for book in results:
                print(" ", book)

        elif choice == "3":
            try:
                title = validate_non_empty(input("  Title: "), "Title")
                author = validate_non_empty(input("  Author: "), "Author")
                year = validate_year(input("  Year: "))
                genre = validate_non_empty(input("  Genre: "), "Genre")
                service.add_book(title, author, year, genre)
            except (ValueError, LibraryError) as e:
                print(f"  Error: {e}")

        elif choice == "4":
            available = service.available_books()
            if not available:
                print("  No books currently available.")
            for book in available:
                print(" ", book)

        elif choice == "5":
            summary = service.genres_summary()
            if not summary:
                print("  No books in the library yet.")
            for genre, count in sorted(summary.items()):
                print(f"  {genre}: {count} book(s)")

        elif choice == "0":
            break
        else:
            print("  Unknown option.")


def menu_users(service: LibraryService) -> None:
    """Sub-menu for user management."""
    while True:
        print_header("USERS")
        print("  1. List all users")
        print("  2. Register a new user")
        print("  0. Back")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            users = service.list_users()
            if not users:
                print("  No users registered yet.")
            for user in users:
                print(" ", user)

        elif choice == "2":
            try:
                name = validate_non_empty(input("  Full name: "), "Name")
                email = validate_email(input("  Email: "))
                service.add_user(name, email)
            except (ValueError, LibraryError) as e:
                print(f"  Error: {e}")

        elif choice == "0":
            break
        else:
            print("  Unknown option.")


def menu_loans(service: LibraryService) -> None:
    """Sub-menu for borrowing and returning books."""
    while True:
        print_header("LOANS")
        print("  1. Borrow a book")
        print("  2. Return a book")
        print("  3. List active loans")
        print("  4. Check overdue loans (>30 days)")
        print("  0. Back")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            try:
                user_id = get_int("  User ID: ")
                book_id = get_int("  Book ID: ")
                service.borrow_book(user_id, book_id)
                print("  Book successfully borrowed.")
            except LibraryError as e:
                print(f"  Error: {e}")

        elif choice == "2":
            try:
                user_id = get_int("  User ID: ")
                book_id = get_int("  Book ID: ")
                service.return_book(user_id, book_id)
                print("  Book successfully returned.")
            except LibraryError as e:
                print(f"  Error: {e}")

        elif choice == "3":
            loans = service.active_loans()
            if not loans:
                print("  No active loans.")
            for loan in loans:
                user = service.users.get(loan.user_id)
                book = service.books.get(loan.book_id)
                u_name = user.name if user else "?"
                b_title = book.title if book else "?"
                print(f"  Loan #{loan.loan_id}: {u_name} has '{b_title}' since {loan.loan_date}")

        elif choice == "4":
            # Using the generator: we iterate over it with a for loop
            warnings = list(service.overdue_warnings(max_days=30))
            if not warnings:
                print("  No overdue loans.")
            for warning in warnings:
                print(warning)

        elif choice == "0":
            break
        else:
            print("  Unknown option.")


def main() -> None:
    """Main function — initialises the service and runs the main menu loop."""
    service = LibraryService()
    print("\nWelcome to Mini Library!")

    while True:
        print_header("MAIN MENU")
        print("  1. Books")
        print("  2. Users")
        print("  3. Loans")
        print("  0. Exit")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            menu_books(service)
        elif choice == "2":
            menu_users(service)
        elif choice == "3":
            menu_loans(service)
        elif choice == "0":
            print("\nGoodbye!\n")
            break
        else:
            print("  Unknown option. Please enter 1, 2, 3 or 0.")


if __name__ == "__main__":
    main()
