import pytest
from src.sequential import download_file, process_file, run_sequential

def test_download_file():
    # Simulated sleep delays downloading pseudo-network requests
    result = download_file("http://example.com/mock_image_1.jpg")
    assert result == "mock_image_1.jpg"
    
def test_process_file():
    # Mathematical sum algorithms simulating heavy CPU locks
    result = process_file("mock_image_1.jpg")
    assert result > 1000

def test_run_sequential():
    # Sequential verification of executing multiple loads linearly
    urls = ["http://example.com/f1.jpg", "http://example.com/f2.jpg"]
    results = run_sequential(urls)
    assert len(results) == 2
