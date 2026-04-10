import os
import multiprocessing
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import List
from .sequential import download_file, process_file

def init_worker():
    """Initializes standard Python logging environments safely inside spawned OS processes."""
    import logging
    logging.basicConfig(level=logging.INFO)
    logging.info(f"Initialized isolated python worker process on PID: {os.getpid()}")

def _process_url_isolated(url: str) -> int:
    """Wrapped standalone method enabling Windows python Multiprocessing execution scopes safely."""
    import logging
    logging.info(f"Starting processing task for {url}")
    filename = download_file(url)
    return process_file(filename)

def process_urls_multiprocessed(urls: List[str]) -> List[int]:
    results = []
    
    # Utilizing entirely independent OS level hardware threads avoiding Python's Global Interpreter Lock
    with ProcessPoolExecutor(max_workers=3, initializer=init_worker) as executor:
        futures = [executor.submit(_process_url_isolated, url) for url in urls]
        for future in as_completed(futures):
            results.append(future.result())
            
    return results
