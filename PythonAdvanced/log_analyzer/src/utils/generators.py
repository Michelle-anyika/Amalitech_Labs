import itertools
from typing import Iterator, List, Dict, Iterable
from src.parser.regex_extractor import LogEntry

def read_large_log(file_path: str) -> Iterator[str]:
    """Memory-safe iterable loading structure for vast log inputs."""
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            yield line

def group_logs_by_status(entries: Iterable[LogEntry]) -> Dict[int, List[LogEntry]]:
    """Implements itertools.groupby clustering algorithms over LogEntry streams."""
    # Itertools demands pre-sorting structures otherwise matching sequence gaps fail
    sorted_entries = sorted(entries, key=lambda e: e.status)
    
    grouped = {}
    for key, group in itertools.groupby(sorted_entries, key=lambda e: e.status):
        grouped[key] = list(group)
    return grouped
