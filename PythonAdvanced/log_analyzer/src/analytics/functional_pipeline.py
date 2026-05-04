import json
import itertools
from functools import reduce
from typing import Iterable, List, Dict, Iterator
from src.parser.regex_extractor import parse_log_line, LogEntry

def map_to_entries(lines: Iterable[str]) -> Iterator[LogEntry]:
    """Maps raw strings to LogEntry objects. Filters out invalid matches."""
    return filter(None, map(parse_log_line, lines))

def filter_by_status(entries: Iterable[LogEntry], min_status: int = 400) -> Iterator[LogEntry]:
    """Filters entries by status code using functional lambda."""
    return filter(lambda entry: entry.status >= min_status, entries)

def sum_bytes(entries: Iterable[LogEntry]) -> int:
    """Calculates total bytes using reduce."""
    return reduce(lambda acc, entry: acc + entry.bytes, entries, 0)

def get_status_distribution(entries: Iterable[LogEntry]) -> Dict[int, int]:
    """Uses itertools.groupby to categorize status code frequencies."""
    # Grouping requires sorted data
    sorted_entries = sorted(entries, key=lambda x: x.status)
    distribution = {}
    for status, group in itertools.groupby(sorted_entries, key=lambda x: x.status):
        distribution[status] = len(list(group))
    return distribution

def write_summary_json(stats: Dict, output_path: str) -> None:
    """Serializes analytic results to a structured JSON file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=4)
