#query/utils.py
from typing import Callable, Iterable, List, Any
from functools import wraps
from typing import Type, Union, Iterable, get_args, get_origin
from ..types import SQLCol, SQLExpression
def _resolve_types(monotype):
    """Helper to resolve a monotype or Union into real runtime types."""
    if monotype is None:
        return None
    types = enlist(monotype)
    final_types = []
    for t in types:
        # If it's a typing.Union[...] — unwrap it
        if get_origin(t) is Union:
            final_types.extend(get_args(t))
        else:
            final_types.append(t)
    return final_types

def normalize_args(skip: int = 0, decompose_string=False, decompose_bytes=False, convert=True, ignore_dict=True):
    """
    Decorator to normalize *args into a list, skipping the first `skip` arguments.
    If a single iterable (not a string) is passed as *args, it will be unpacked.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            skipped_args = args[:skip]
            target_args = args[skip:] if len(args) > skip else ()

            normalized_args = _normalize_args(
                *target_args,
                decompose_string=decompose_string,
                decompose_bytes=decompose_bytes,
                convert=convert,
                ignore_dict=ignore_dict
            )

            return func(*skipped_args, *normalized_args, **kwargs)
        return wrapper
    return decorator


def _normalize_args(*args, decompose_string=False, decompose_bytes=False, convert=True, ignore_dict=True):

    if not args:
        return []
    elif len(args) > 1:
        return list(args)
    if isinstance(args[0], str):
        if decompose_string:
            return list(args[0])
        return [args[0]]
    elif isinstance(args[0], bytes):
        if decompose_bytes:
            return list(args[0])
        return [args[0]] 
    elif isinstance(args[0], dict):
        if ignore_dict:
            return [args[0]]
        return list(args[0].values())
    elif isinstance(args[0], Iterable) and not isinstance(args[0], (str, bytes)):
        #Second check should never happen, but just in case someone alters the function
        if convert:
            return list(args[0])
        return args[0]
    else:

        return list(args)
    
def enlist(items, decompose_string=False, decompose_bytes=True, *, unpack=True) -> list:
    if any((
        isinstance(items, str) and decompose_string,
        isinstance(items, bytes) and decompose_bytes,
        (unpack and isinstance(items, Iterable) and not isinstance(items, (str, bytes)))
    )):
        return list(items)
    
    return [items]

def validate_monolist(*items, monotype: Union[Iterable[Type], Type] = None) -> None:
    """
    Validates that all items are of the same type, within the allowed `monotype` set (if provided).
    """
    if len(items) <= 1:
        return

    monotype = _resolve_types(monotype) if monotype is not None else [type(items[0])]
    if not all(isinstance(t, type) for t in monotype):
        raise TypeError("All elements in 'monotype' must be types.")

    first_item = items[0]
    try:
        type_to_verify = next(_type for _type in monotype if isinstance(first_item, _type))
    except StopIteration:
        raise TypeError(
            f"First item {first_item} is not an instance of any allowed monotypes: {monotype}"
        )

    for i, item in enumerate(items[1:], start=1):
        if not isinstance(item, type_to_verify):
            raise TypeError(
                f"Item {i} is of type {type(item).__name__}, expected {type_to_verify.__name__}."
            )

def is_pair(item: Any) -> bool:
    """
    Check if the item is a pair (tuple or list of length 2).
    """
    return isinstance(item, (tuple, list)) and len(item) == 2

def get_col_value(col:SQLCol):
    """
    Get the value of a column, which can be a string or SQLExpression.
    """
    if isinstance(col, SQLExpression):
        return col.expression_value
    elif isinstance(col, str):
        return col
    else:
        raise TypeError("Column must be a string or SQLExpression.")