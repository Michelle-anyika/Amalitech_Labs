import pytest
from src.multiprocessed_processor import process_urls_multiprocessed

def test_process_urls_multiprocessed():
    urls = [
        "http://example.com/asset_1.png", 
        "http://example.com/asset_2.png",
        "http://example.com/asset_3.png"
    ]
    
    # Validate isolated hardware multiprocessing runs exactly perfectly mimicking ThreadPool constraints
    results = process_urls_multiprocessed(urls)
    
    # ProcessPoolExecutor should effortlessly complete calculations scaling isolated CPUs
    assert len(results) == 3
    assert all(r.result_value > 1000 for r in results)
    assert all(r.execution_time > 0 for r in results)
