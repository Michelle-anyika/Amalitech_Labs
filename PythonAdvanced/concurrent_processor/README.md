# Lab 3: Concurrent File Processor

An intelligent benchmarking Python architecture implementing simulated hardware downloads and mathematical CPU restrictions highlighting the limitations and structures natively wrapping threading and multiprocessing logic!

## Performance Graph & Comparison
Testing 25 intensive mathematical items across the environments resulted in these physical benchmarking execution spans:

| Methodology | Time | Python Implementation Details |
|-------------|------|----------------------------------------------------|
| Sequential | **5.48s** | `for url in urls: download() ... process()` |
| ThreadPoolExecutor | **2.84s** | Resolves `download()` I/O natively but bottlenecks Python's Global Interpreter Lock strictly blocking raw CPU mathematics context switches. |
| ProcessPoolExecutor | **2.33s** | Complete OS-Level isolated processor execution bypassing GIL overhead utilizing max computer cores securely via `<logging>` initializers. |
| Asyncio Event Loop | **3.30s** | Scalable `asyncio.gather` I/O sweeps mapping CPU work down strictly into isolated background `run_in_executor` loops contexts. |

## Usage Decision Guide (When to Use Threads vs Multiplexing)
- **Use Threading (`ThreadPoolExecutor`)** or **Asyncio**: Highly applicable when scraping websites natively, interacting with disk writes, or listening via socket I/O loops. Threading restricts CPU utilization identically per the **GIL** meaning true mathematical processing scales don't happen automatically limit-bound.
- **Use Multiprocessing (`ProcessPoolExecutor`)**: The absolute requirement when resolving complex math sequences natively (like image processing masks and video generation models) because we bypass the single process limitations and fork standard memory heaps across completely independent concurrent processes mapped strictly by your system's hardware core limits!
