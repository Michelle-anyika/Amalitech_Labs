import pytest
import asyncio
from src.async_processor import process_urls_async

def test_asyncio_processor():
    urls = [
        "http://example.com/asset_async_1.png",
        "http://example.com/asset_async_2.png"
    ]
    
    # Resolving non-blocking asynchronous loops natively
    results = asyncio.run(process_urls_async(urls))
    assert len(results) == 2
