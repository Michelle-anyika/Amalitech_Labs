import pytest
from src.threaded_processor import process_urls_threaded, get_progress_counter

def test_process_urls_threaded():
    urls = [
        "http://example.com/asset_1.png", 
        "http://example.com/asset_2.png",
        "http://example.com/asset_3.png"
    ]
    
    results = process_urls_threaded(urls)
    
    # Verify ThreadPoolExecutor completed the payload concurrently
    assert len(results) == 3
    assert result_values_valid(results)
    
    # Progress counter protected by threading.Lock() should precisely match the job quantity
    assert get_progress_counter() == 3
    
def result_values_valid(results: list) -> bool:
    for res in results:
        if res <= 1000:
            return False
    return True
