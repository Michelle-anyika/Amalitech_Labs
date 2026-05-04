import os
import time
import multiprocessing
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import List
from .sequential import download_file, process_file
from .dataset import ProcessingResult

def init_worker():
    """Initializes standard Python logging environments safely inside spawned OS processes."""
    import logging
    logging.basicConfig(level=logging.INFO)
    logging.info(f"Initialized isolated python worker process on PID: {os.getpid()}")

def _process_url_isolated(url: str) -> ProcessingResult:
    """Wrapped standalone method enabling Windows python Multiprocessing execution scopes safely."""
    import logging
    start_time = time.time()
    logging.info(f"Starting processing task for {url}")
    filename = download_file(url)
    val = process_file(filename)
    duration = time.time() - start_time
    return ProcessingResult(
        url=url,
        filename=filename,
        result_value=val,
        execution_time=duration
    )

def process_urls_multiprocessed(urls: List[str]) -> List[ProcessingResult]:
    results = []
    
    # Utilizing entirely independent OS level hardware threads avoiding Python's Global Interpreter Lock
    with ProcessPoolExecutor(max_workers=3, initializer=init_worker) as executor:
        futures = [executor.submit(_process_url_isolated, url) for url in urls]
        for future in as_completed(futures):
            results.append(future.result())
            
    return results
