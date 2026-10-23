# Mini Library — s36150

A command-line library management system written in Python.

## Features

- Add and search books
- Register library members
- Borrow and return books
- Detect overdue loans
- All data persisted to a JSON file

## Project Structure

```
s36150_projekt/
├── main.py               # Entry point, CLI menu
├── README.md
│
├── models/
│   ├── book.py           # Book class
│   ├── user.py           # User class
│   └── loan.py           # Loan class
│
├── services/
│   ├── library_service.py  # Core business logic
│   └── file_service.py     # JSON read/write
│
├── utils/
│   ├── decorators.py     # @log_action decorator
│   ├── validators.py     # Regex-based input validation
│   └── exceptions.py     # Custom exception classes
│
└── data/
    └── library.json      # Persistent data storage
```

## How to Run

Python 3.10 or newer is required (no external libraries needed).

```bash
cd s36150_projekt
python main.py
```

## Python Language Elements Used

| Element | Location |
|---|---|
| Classes | `models/book.py`, `models/user.py`, `models/loan.py` |
| Control statements (if, for, while) | `main.py`, `services/library_service.py` |
| Operators (arithmetic, logical, comparison) | `services/library_service.py` |
| Functions + lambda | `services/library_service.py` (e.g. `list_books`, `list_users`) |
| Custom decorator | `utils/decorators.py` → `@log_action` |
| Collections (list, dict, set) | `services/library_service.py` — `self.books`, `self.users`, `self.loans` |
| List comprehension | `services/library_service.py` — `search_books`, `available_books` |
| Dict comprehension | `services/library_service.py` — `genres_summary` |
| Set comprehension | `services/library_service.py` — `genres_summary` (genres set) |
| Generator function | `services/library_service.py` — `overdue_warnings` |
| File handling + `with` | `services/file_service.py` |
| JSON serialization | `services/file_service.py`, `models/*.py` (`to_dict` / `from_dict`) |
| Regular expressions | `utils/validators.py` — email and year validation |
| Custom exceptions | `utils/exceptions.py` — `BookNotFoundError`, `UserNotFoundError`, etc. |
