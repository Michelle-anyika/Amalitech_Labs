import time
import json
import asyncio
import statistics
from collections import Counter
from src.dataset import URLS, ProcessingResult
from src.sequential import run_sequential
from src.threaded_processor import process_urls_threaded
from src.multiprocessed_processor import process_urls_multiprocessed
from src.async_processor import process_urls_async

def analyze_results(strategy_name: str, results: list[ProcessingResult], total_duration: float):
    """Analyzes a batch of results using collections and statistics modules."""
    execution_times = [r.execution_time for r in results]
    result_values = [r.result_value for r in results]
    
    # Categorize results using Counter (e.g., by range)
    # result_value is usually around 666666166 or similar
    value_distribution = Counter([v // 100_000_000 for v in result_values])
    
    analysis = {
        "strategy": strategy_name,
        "total_benchmark_time": round(total_duration, 4),
        "avg_item_time": round(statistics.mean(execution_times), 4),
        "median_item_time": round(statistics.median(execution_times), 4),
        "stdev_item_time": round(statistics.stdev(execution_times), 4) if len(execution_times) > 1 else 0,
        "value_ranges_counts": {f"{k*100}M-{ (k+1)*100}M": v for k, v in value_distribution.items()}
    }
    return analysis

async def run_benchmarks():
    print(f"Starting benchmarks for {len(URLS)} items...")
    all_stats = []

    # 1. Sequential
    start = time.time()
    res_seq = run_sequential(URLS)
    all_stats.append(analyze_results("Sequential", res_seq, time.time() - start))
    print("Sequential complete.")

    # 2. Threaded
    start = time.time()
    res_thread = process_urls_threaded(URLS)
    all_stats.append(analyze_results("ThreadPool", res_thread, time.time() - start))
    print("ThreadPool complete.")

    # 3. Multiprocessing
    start = time.time()
    res_multi = process_urls_multiprocessed(URLS)
    all_stats.append(analyze_results("ProcessPool", res_multi, time.time() - start))
    print("ProcessPool complete.")

    # 4. Asyncio
    start = time.time()
    res_async = await process_urls_async(URLS)
    all_stats.append(analyze_results("Asyncio", res_async, time.time() - start))
    print("Asyncio complete.")

    # Write results to JSON
    with open("benchmark_results.json", "w", encoding="utf-8") as f:
        json.dump(all_stats, f, indent=4)
    
    print("\nBenchmark results saved to benchmark_results.json")
    for stat in all_stats:
        print(f"{stat['strategy']}: {stat['total_benchmark_time']}s")

if __name__ == "__main__":
    asyncio.run(run_benchmarks())
