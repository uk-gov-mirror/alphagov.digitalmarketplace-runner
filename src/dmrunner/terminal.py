import blessed
import click
from invoke.exceptions import Exit

from functools import wraps

terminal = blessed.Terminal()

def catch_abort(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except click.exceptions.Abort:
            print()
            raise Exit
    return wrapper

prompt = catch_abort(click.prompt)
confirm = catch_abort(click.confirm)
