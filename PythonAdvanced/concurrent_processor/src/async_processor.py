import asyncio
import math
from typing import List

async def download_file_async(url: str) -> str:
    """Non-blocking asynchronous I/O sleeps enabling event loop pass-through natively."""
    await asyncio.sleep(0.1)
    return url.split("/")[-1]

def process_file_sync(filename: str) -> int:
    result = 0
    for i in range(1_000_000):
        result += math.isqrt(i)
    return result

async def process_url_async_block(url: str) -> int:
    filename = await download_file_async(url)
    
    # Delegating CPU blocking mathematics to native background thread executors safely out of the standard event loop limits
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, process_file_sync, filename)
    return result

async def process_urls_async(urls: List[str]) -> List[int]:
    """Generates execution blocks and batches resolutions identically off asyncio gathers"""
    tasks = [process_url_async_block(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return results
