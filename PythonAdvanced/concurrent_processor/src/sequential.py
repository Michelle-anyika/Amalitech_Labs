import time
import math
from typing import List

def download_file(url: str) -> str:
    """Simulates an I/O Network bounding condition by aggressively sleeping."""
    time.sleep(0.1)
    return url.split("/")[-1]

def process_file(filename: str) -> int:
    """Simulates an extremely aggressive CPU bound mathematical lock."""
    # Sum of square roots creates direct CPU hardware utilization overhead blocking execution lengths
    result = 0
    for i in range(1_000_000):
        result += math.isqrt(i)
    return result

def run_sequential(urls: List[str]) -> List[int]:
    """Generates standard baseline sequential executions running strictly one-by-one."""
    results = []
    for url in urls:
        filename = download_file(url)
        processed = process_file(filename)
        results.append(processed)
    return results
