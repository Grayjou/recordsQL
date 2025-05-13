
from typing import Callable
from dataclasses import dataclass
from collections.abc import Iterable
from types import GeneratorType
def is_collection(thing:Iterable) -> bool:
    """
    Check if the given thing is a collection (list, tuple, set, etc.).
    Args:
        thing: The object to check.
    Returns:
        bool: True if the object is a collection, False otherwise.
    """
    return isinstance(thing, Iterable) and not isinstance(thing, (bytes, str, GeneratorType))

def is_unknown(value) -> bool:
        """
        Check if the value is an instance of Unknown.
        Args:
            value: The value to check.
        Returns:
            bool: True if the value is an instance of Unknown, False otherwise.
        """
        return isinstance(value, Unknown)

@dataclass(frozen=True)
class Unknown:
    name: str = "value"

    def __repr__(self):
        return f"Unknown({self.name})"

    __str__ = __repr__

    def __eq__(self, other):
        return is_unknown(other) and self.name == other.name

    def _raise_compare_error(self, *args, **kwargs):
        raise ValueError("Cannot compare Unknown type")

    __lt__ = __le__ = __gt__ = __ge__ = _raise_compare_error

    def __bool__(self):
        return False
    
    @staticmethod
    def is_unknown(value) -> bool:
        """
        Check if the value is an instance of Unknown.
        Args:
            value: The value to check.
        Returns:
            bool: True if the value is an instance of Unknown, False otherwise.
        """
        return is_unknown(value)

unknown = Unknown()
def none_or_unknown(value) -> bool:
    """
    Check if the value is None or an instance of Unknown.
    Args:
        value: The value to check.
    Returns:
        bool: True if the value is None or an instance of Unknown, False otherwise.
    """
    return value is None or is_unknown(value)

def quote_str(value: str, quote_char: str = '"') -> str:
    """
    Quote a string with the specified quote character.
    Args:
        value (str): The string to quote.
        quote_char (str): The character to use for quoting. Defaults to '"'.
    Returns:
        str: The quoted string.
    """
    return f"{quote_char}{value}{quote_char}" if value else ""

def keys_exist_in_dict(d: dict, keys: Iterable[str]) -> bool:
    return all(key in d for key in keys)

def bracket_str(value: str, left_bracket: str = "(", right_bracket: str = ")") -> str:
    """
    Enclose a string with the specified brackets.
    Args:
        value (str): The string to enclose.
        left_bracket (str): The character to use for the left bracket. Defaults to '('.
        right_bracket (str): The character to use for the right bracket. Defaults to ')'.
    Returns:
        str: The enclosed string.
    """
    return f"{left_bracket}{value}{right_bracket}" if value else ""

def str_is_between(value: str, start: str, end: str) -> bool:
    """
    Check if a string is between two other strings.
    Args:
        value (str): The string to check.
        start (str): The starting string.
        end (str): The ending string.
    Returns:
        bool: True if the value is between start and end, False otherwise.
    """
    return value.startswith(start) and value.endswith(end)

def ensure_bracketed(value: str, left_bracket: str = "(", right_bracket: str = ")") -> str:
    """
    Ensure a string is enclosed with the specified brackets.
    Args:
        value (str): The string to check.
        left_bracket (str): The character to use for the left bracket. Defaults to '('.
        right_bracket (str): The character to use for the right bracket. Defaults to ')'.
    Returns:
        str: The enclosed string.
    """
    if not str_is_between(value, left_bracket, right_bracket):
        return bracket_str(value, left_bracket, right_bracket)
    return value

class All:
    
    def __init__(self):
        pass    
    def __eq__(self, value):
        return isinstance(value, All)
    
