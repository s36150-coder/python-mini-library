"""
Custom decorators for the Mini Library system.

A decorator is a function that wraps another function to add extra behaviour
without modifying the original function's code.

Usage:  @log_action
        def some_function(...): ...

When some_function() is called, the wrapper runs first, then calls the
original function, and finally prints the result.
"""
import functools


def log_action(func):
    """
    Decorator that prints a log message every time a service method is called.

    This is genuinely useful: in a real library system you would want an audit
    trail of every borrow / return / add operation.
    """
    @functools.wraps(func)   # keeps the original function's name and docstring
    def wrapper(*args, **kwargs):
        print(f"  [LOG] Calling: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"  [LOG] Done:    {func.__name__}")
        return result
    return wrapper
