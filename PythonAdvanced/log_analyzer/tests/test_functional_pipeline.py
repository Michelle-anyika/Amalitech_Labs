import pytest
from src.analytics.functional_pipeline import map_to_dicts, filter_by_status, sum_bytes

def test_map_to_dicts():
    lines = [
        '192.168.1.1 - - [10/Oct:13:55:36 -0700] "GET / HTTP/1.1" 200 100',
        'Invalid line that skips and should cleanly omit',
        '10.0.0.1 - - [10/Oct:13:56:00 -0700] "POST /api HTTP/1.1" 404 200'
    ]
    # Functional map
    dicts = list(map_to_dicts(lines))
    assert len(dicts) == 2
    assert dicts[0]['status'] == '200'
    assert dicts[1]['status'] == '404'
    
def test_filter_by_status():
    dicts = [
        {'status': '200', 'bytes': '100'},
        {'status': '404', 'bytes': '200'},
        {'status': '500', 'bytes': '300'}
    ]
    # Filter only 400+ errors functionally
    errors = list(filter_by_status(dicts, min_status=400))
    assert len(errors) == 2
    assert errors[0]['status'] == '404'
    
def test_sum_bytes():
    dicts = [{'bytes': '100'}, {'bytes': '200'}, {'bytes': '300'}]
    # functools reduce combination
    total = sum_bytes(dicts)
    assert total == 600
