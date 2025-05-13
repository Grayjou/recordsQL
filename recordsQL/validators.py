
from os import path as os_path_basename
from .utils import unknown, All
import re
from functools import wraps
from inspect import signature
from .types import SQLCol
from typing import Any, Union, Iterable, Callable, List
from .dependencies import SQLExpression
def validate_table_name(func, table_name_position: int = 0, *,
    validate_chars: bool = True, 
    validate_words: bool = True, 
    validate_len: bool = True,
    allow_dot: bool = True,
    allow_dollar: bool = False,
    max_len: int = 255,
    forgiven_chars = set(),
    allow_digit: bool = False,):
    """
    Decorator to validate the 'table_name' argument.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        bound_args = signature(func).bind_partial(*args, **kwargs)
        bound_args.apply_defaults()

        if 'table_name' in bound_args.arguments:
            table_name = bound_args.arguments['table_name']
        elif len(args) > table_name_position:
            table_name = args[table_name_position]
        else:
            raise ValueError("No 'table_name' argument found to validate.")

        validate_name(table_name,
                      validate_chars=validate_chars,
                      validate_words=validate_words,
                      validate_len=validate_len,
                      allow_dot=allow_dot,
                      allow_dollar=allow_dollar,
                      max_len=max_len,
                      forgiven_chars=forgiven_chars,
                      allow_digit=allow_digit)
        return func(*args, **kwargs)

    return wrapper
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


# Reserved device names on Windows (case-insensitive)
WINDOWS_RESERVED_NAMES = {
    "CON", "PRN", "AUX", "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10))
}

# Disallowed characters on Windows & common CLI contexts
ILLEGAL_CHARS_PATTERN = re.compile(r'[<>:"/\\|?*\x00-\x1F]')  # \x00-\x1F = control chars

def validate_file_name(file_name: str, *, return_false_on_error: bool = False, remove_suffix: bool = False) -> bool:
    """
    Validates a file name to ensure it is safe for filesystem and console usage.
    
    Args:
        file_name (str): The file name to validate.
        return_false_on_error (bool): If True, returns False instead of raising on error.
        remove_suffix (bool): If True, removes the file extension before validation.

    Returns:
        bool: True if the file name is valid; False if invalid and return_false_on_error is True.

    Raises:
        ValueError: If validation fails and return_false_on_error is False.
    """
    try:
        if not isinstance(file_name, str):
            raise ValueError("file_name must be a string")

        file_name = os_path_basename(file_name)

        if remove_suffix:
            dot_index = file_name.rfind(".")
            if dot_index > 0:
                file_name = file_name[:dot_index]

        stripped_name = file_name.strip()
        if not stripped_name:
            raise ValueError("file_name cannot be empty or whitespace only")
        if stripped_name.startswith(".") or stripped_name.endswith("."):
            raise ValueError("file_name cannot start or end with a dot")
        if stripped_name in ("/", "\\"):
            raise ValueError("file_name cannot be just a slash")
        if ILLEGAL_CHARS_PATTERN.search(stripped_name):
            raise ValueError("file_name contains illegal characters (e.g. < > : \" / \\ | ? *)")
        if stripped_name.upper() in WINDOWS_RESERVED_NAMES:
            raise ValueError(f"file_name '{file_name}' is reserved on Windows")
        if len(stripped_name) > 255:
            raise ValueError("file_name exceeds maximum length (255 characters)")

    except ValueError:
        if return_false_on_error:
            return False
        else:
            raise

    return True

def validate_database_path(database_path: str, *, return_false_on_error: bool = False) -> bool:
    """
    Validates the given database path to ensure it meets the requirements for a valid SQLite database file.

    Args:
        database_path (str): The path to the SQLite database file.
        return_false_on_error (bool, optional): If True, return False instead of raising exceptions on invalid input. Defaults to False.

    Returns:
        bool: True if the database path is valid; False if invalid and return_false_on_error is True.

    Raises:
        ValueError: If validation fails and return_false_on_error is False.
    """
    try:
        if database_path is None or database_path == unknown:
            return False

        if not isinstance(database_path, str):
            raise ValueError("database_path must be a string")

        file_name = os_path_basename(database_path)

        if not file_name.endswith(".db"):
            raise ValueError("database_path must be a valid SQLite database file (must end with .db)")

        # Validate the filename before the .db
        if not validate_file_name(file_name, return_false_on_error=False, remove_suffix=True):
            raise ValueError("database_path contains an invalid file name before '.db'")

    except ValueError:
        if return_false_on_error:
            return False
        else:
            raise

    return True

keywords = {
        "select", "from", "where", "table", "insert", "update", "delete",
        "create", "drop", "alter", "join", "on", "as", "and", "or", "not",
        "in", "is", "null", "values", "set", "group", "by", "order", "having",
        "limit", "offset", "distinct"
    }

def get_forbidden_words_in(name: str):

    tokens = name.casefold().replace('.', ' ').replace('_', ' ').split()
    return [kw for kw in keywords if kw in tokens]

def validate_name(
    name: str, *, 
    validate_chars: bool = True, 
    validate_words: bool = True, 
    validate_len: bool = True,
    allow_dot: bool = True,
    allow_dollar: bool = False,
    max_len: int = 255,
    forgiven_chars = set(),
    allow_digit: bool = False,
) -> None:
    

    if isinstance(name, SQLExpression) and name.expression_type == "query":
        if getattr(name, "skip_validation", False):
            raise AttributeError("Conflicting attribute: skip_validation at validate_name")
        if getattr(name, "ignore_forbidden_chars", False):
            raise AttributeError("Conflicting attribute: ignore_forbidden_chars at validate_name")
        return
    if not isinstance(name, str):
        raise TypeError("Name must be a string.")

    if is_number(name):
        raise ValueError("Column name cannot be a number.")

    if len(name) == 0:
        raise ValueError("Column name cannot be empty.")

    if validate_len and len(name) > max_len:
        raise ValueError("Column name is too long. Maximum length is 255 characters.")

    if name[0].isdigit() and not allow_digit:
        raise ValueError("Column name cannot start with a digit.")
    
    if validate_chars:
        allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_")
        allowed.update(forgiven_chars)
        if allow_dot:
            allowed.add('.')
        if allow_dollar:
            allowed.add('$')
        
        bad_chars = [c for c in name if c not in allowed]
        if bad_chars:
            raise ValueError(f"Column name contains forbidden characters: {bad_chars}")

        if allow_dot:
            # Extra check: make sure dots are only separating valid parts
            parts = name.split('.')
            for part in parts:
                if not part:
                    raise ValueError("Column name has consecutive dots or leading/trailing dot.")
                if part[0].isdigit():
                    raise ValueError(f"Each part of a dotted name must not start with a digit: {part}")

    if validate_words:
        found = next((word for word in keywords if word == name.casefold()), None)
        if found:
            raise ValueError(f"Name contains forbidden words: {found}")



def must_be_type(obj: Any, type_: Union[type, Iterable[type]], name: str = "argument",
                 must_be_true: bool = False, additional_checks: List[Callable] = None) -> None:
    """
    Validate that the input is of a specific type or types.
    
    Args:
        obj (Any): The input to validate.
        type_ (Union[type, Iterable[type]]): The expected type or types.
        name (str): The name of the argument for error messages.
        must_be_true (bool): If True, raises an error if bool(obj) is False.
        additional_checks (List[Callable]): Additional boolean-returning checks on the object.

    Raises:
        TypeError: If obj is not an instance of type_.
        ValueError: If must_be_true is True and obj is falsy, or if any additional check fails.
    """
    additional_checks = additional_checks or []

    if isinstance(type_, type):
        type_tuple = (type_,)
    elif isinstance(type_, Iterable) and all(isinstance(t, type) for t in type_):
        type_tuple = tuple(type_)
    else:
        raise TypeError("type_ must be a type or an iterable of types.")

    if not isinstance(obj, type_tuple):
        type_names = ", ".join(t.__name__ for t in type_tuple)
        raise TypeError(f"{name} must be of type {type_names}, but got {type(obj).__name__}.")

    if must_be_true and not bool(obj):
        raise ValueError(f"{name} must be truthy, but got {obj!r}.")

    for check in additional_checks:
        if not check(obj):
            raise ValueError(f"{name} failed additional check {check.__name__}: {obj!r}.")



def must_be_str(s: str, name: str = "argument", must_not_be_empty: bool = True) -> str:
    """
    Validate that the input is a string and optionally check if it's not empty.
    """
    must_be_type(s, str, name=name, must_be_true=must_not_be_empty)
    return s

    

def validate_column_name(
    name: SQLCol, *, 
    validate_chars: bool = True, 
    validate_words: bool = True, 
    validate_len: bool = True,
    allow_dot: bool = True,
    allow_dollar: bool = False,
    max_len: int = 255,
    forgiven_chars = set()
) -> None:
    if name in ("*", All()) or list(name) == ["*"]:
        return
    validate_name(
        name, 
        validate_chars=validate_chars, 
        validate_words=validate_words, 
        validate_len=validate_len,
        allow_dot=allow_dot,
        allow_dollar=allow_dollar,
        max_len=max_len,
        forgiven_chars=forgiven_chars
    )

def validate_column_names(names, *, 
    validate_chars: bool = True, 
    validate_words: bool = True, 
    validate_len: bool = True,
    allow_dot: bool = True,
    allow_dollar: bool = False,
    max_len: int = 255,
    forgiven_chars = set()
) -> None:
    if names in ("*", All(), None) or list(names) == ["*"] or any(n in ("*", All()) for n in names):
        return
    if isinstance(names, str):
        names = [names]
    for name in names:
        validate_column_name(
            name, 
            validate_chars=validate_chars, 
            validate_words=validate_words, 
            validate_len=validate_len,
            allow_dot=allow_dot,
            allow_dollar=allow_dollar,
            max_len=max_len,
            forgiven_chars=forgiven_chars
        )