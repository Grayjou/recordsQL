from typing import Type, Union, Iterable

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
    
    If `monotype` is given, it should be a single type or an iterable of acceptable types.
    Raises TypeError if any item differs from the determined monotype.
    """
    if len(items) <= 1:
        return

    monotype = enlist(monotype) if monotype is not None else [type(items[0])]
    if not all(isinstance(t, type) for t in monotype):
        raise TypeError("All elements in 'monotype' must be types.")

    first_item = items[0]
    try:
        type_to_verify = next(_type for _type in monotype if isinstance(first_item, _type))
    except StopIteration:
        raise TypeError(f"First item {first_item} is not an instance of any allowed monotypes: {monotype}")

    for i, item in enumerate(items[1:], start=1):
        if not isinstance(item, type_to_verify):
            raise TypeError(f"Item {i} is of type {type(item).__name__}, expected {type_to_verify.__name__}.")

