import pytest
from src.analytics.functional_pipeline import map_to_entries, filter_by_status, sum_bytes
from src.parser.regex_extractor import LogEntry

def test_map_to_entries():
    lines = [
        '192.168.1.1 - - [10/Oct:13:55:36 -0700] "GET / HTTP/1.1" 200 100',
        'Invalid line that skips and should cleanly omit',
        '10.0.0.1 - - [10/Oct:13:56:00 -0700] "POST /api HTTP/1.1" 404 200'
    ]
    # Functional map
    entries = list(map_to_entries(lines))
    assert len(entries) == 2
    assert entries[0].status == 200
    assert entries[1].status == 404
    
def test_filter_by_status():
    entries = [
        LogEntry('1.1.1.1', 'now', 'GET', '/', 200, 100),
        LogEntry('1.1.1.1', 'now', 'GET', '/', 404, 200),
        LogEntry('1.1.1.1', 'now', 'GET', '/', 500, 300)
    ]
    # Filter only 400+ errors functionally
    errors = list(filter_by_status(entries, min_status=400))
    assert len(errors) == 2
    assert errors[0].status == 404
    
def test_sum_bytes():
    entries = [
        LogEntry('1.1.1.1', 'now', 'GET', '/', 200, 100),
        LogEntry('1.1.1.1', 'now', 'GET', '/', 200, 200),
        LogEntry('1.1.1.1', 'now', 'GET', '/', 200, 300)
    ]
    # functools reduce combination
    total = sum_bytes(entries)
    assert total == 600
