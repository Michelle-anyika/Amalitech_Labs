from functools import reduce
from typing import Iterable, Dict, Iterator
from src.parser.regex_extractor import parse_log_line

def map_to_dicts(lines: Iterable[str]) -> Iterator[Dict[str, str]]:
    """Maps array of raw strings strictly down to extracted named groups dicts. Cleans missing logic via filters."""
    # Maps every string to the parse output
    mapped = map(parse_log_line, lines)
    # Filter strips out Nones returned from the map if regex matching fails
    return filter(None, mapped)

def filter_by_status(dicts: Iterable[Dict[str, str]], min_status: int = 400) -> Iterator[Dict[str, str]]:
    """Filters functional structures comparing numerical cast conditionals."""
    return filter(lambda dict: int(dict.get('status', '0')) >= min_status, dicts)

def sum_bytes(dicts: Iterable[Dict[str, str]]) -> int:
    """Consumes the Iterable payload chaining aggregations functionally."""
    return reduce(lambda acc, dict: acc + int(dict.get('bytes', '0')), dicts, 0)
