import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List
from .sequential import download_file, process_file
from .dataset import ProcessingResult

# Global shared variables demonstrating thread-safety implementations
progress_counter = 0
counter_lock = threading.Lock()

def get_progress_counter() -> int:
    global progress_counter
    with counter_lock:
        return progress_counter

def process_url_task(url: str) -> ProcessingResult:
    global progress_counter
    start_time = time.time()
    
    # I/O Bound
    filename = download_file(url)
    
    # CPU Bound
    val = process_file(filename)
    
    # Securely modify explicit state using Python Lock mechanics!
    with counter_lock:
        progress_counter += 1
        
    duration = time.time() - start_time
    return ProcessingResult(
        url=url,
        filename=filename,
        result_value=val,
        execution_time=duration
    )

def process_urls_threaded(urls: List[str]) -> List[ProcessingResult]:
    results = []
    
    # Utilize Python threads seamlessly masking execution complexities
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(process_url_task, url) for url in urls]
        for future in as_completed(futures):
            results.append(future.result())
            
    return results
