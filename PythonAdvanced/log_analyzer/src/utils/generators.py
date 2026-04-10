import itertools
from typing import Iterator, Dict, Iterable

def read_large_log(file_path: str) -> Iterator[str]:
    """Memory-safe iterable loading structure for vast log inputs."""
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            yield line

def group_logs_by_status(dicts: Iterable[Dict[str, str]]) -> Dict[str, list]:
    """Implements itertools.groupby clustering algorithms over parsed JSON arrays."""
    # Itertools demands pre-sorting structures otherwise matching sequence gaps fail
    sorted_dicts = sorted(dicts, key=lambda d: d.get('status', '0'))
    
    grouped = {}
    for key, group in itertools.groupby(sorted_dicts, key=lambda d: d.get('status', '0')):
        grouped[key] = list(group)
    return grouped
