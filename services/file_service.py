"""
File service — handles reading and writing JSON data files.

The 'with' statement (context manager) is used here.
It guarantees that the file is properly closed even if an error occurs.
"""
import json
import os


def load_json(filepath: str) -> dict:
    """
    Load data from a JSON file.
    If the file does not exist yet, return a default empty structure.
    """
    if not os.path.exists(filepath):
        return {"books": [], "users": [], "loans": []}

    with open(filepath, "r", encoding="utf-8") as f:   # <-- context manager
        return json.load(f)


def save_json(filepath: str, data: dict) -> None:
    """
    Save data to a JSON file with pretty formatting.
    The 'with' block ensures the file handle is closed after writing.
    """
    with open(filepath, "w", encoding="utf-8") as f:   # <-- context manager
        json.dump(data, f, indent=4, ensure_ascii=False)
