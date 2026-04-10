import pytest
from src.parser.regex_extractor import parse_log_line, clean_log

def test_parse_valid_log_line():
    line = '192.168.1.1 - - [10/Oct/2023:13:55:36 -0700] "GET /index.html HTTP/1.1" 200 2326'
    result = parse_log_line(line)
    
    assert result is not None
    assert result['ip'] == '192.168.1.1'
    assert result['timestamp'] == '10/Oct/2023:13:55:36 -0700'
    assert result['method'] == 'GET'
    assert result['url'] == '/index.html'
    assert result['status'] == '200'
    
def test_parse_invalid_log_line():
    line = 'This is completely malformed noise without structures'
    result = parse_log_line(line)
    assert result is None
    
def test_clean_log():
    dirty_log_string = 'GET /search?q=bad%20string%20<script>alert(1)</script> HTTP/1.1'
    cleaned = clean_log(dirty_log_string)
    
    # Ensuring dangerous HTML and script brackets are substituted via re.sub
    assert '<' not in cleaned
    assert '>' not in cleaned
    assert 'script' not in cleaned
