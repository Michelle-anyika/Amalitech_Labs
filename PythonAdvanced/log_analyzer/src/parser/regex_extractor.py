import re
from typing import Dict, Optional

# Match Apache format via extensive Named Groups
LOG_PATTERN = re.compile(
    r'^(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) '
    r'- - \[(?P<timestamp>.*?)\] '
    r'"(?P<method>[A-Z]+) (?P<url>[^\s]+)[^"]*" '
    r'(?P<status>\d{3}) (?P<bytes>\d+)$'
)

def parse_log_line(line: str) -> Optional[Dict[str, str]]:
    """Takes a raw log line, searches via compilation, returns mapped dict."""
    match = LOG_PATTERN.match(line)
    if match:
        return match.groupdict()
    return None

def clean_log(line: str) -> str:
    """Removes bad malicious tags injected into logs using re.sub()"""
    # Replace anything resembling an HTML tag <...> with empty string
    cleaned = re.sub(r'<[^>]+>', '', line)
    # Simplify any double spaces caused by missing text to single spaces
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned
