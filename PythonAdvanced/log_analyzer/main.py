import sys
import os
from src.parser.regex_extractor import clean_log
from src.analytics.functional_pipeline import (
    map_to_entries, 
    filter_by_status, 
    sum_bytes, 
    get_status_distribution,
    write_summary_json
)

def log_generator(file_path):
    """Generator to read large files line-by-line efficiently."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                yield clean_log(line)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied when reading '{file_path}'.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

def main():
    log_file = os.path.join("data", "server.log")
    output_file = "summary.json"

    print(f"Starting analysis of {log_file}...")

    # Initialize generator
    lines = log_generator(log_file)

    # Process pipeline
    entries = list(map_to_entries(lines))
    
    total_bytes = sum_bytes(entries)
    status_dist = get_status_distribution(entries)
    error_entries = list(filter_by_status(entries, 400))

    # Prepare stats
    stats = {
        "total_entries": len(entries),
        "total_bytes_transferred": total_bytes,
        "status_distribution": {str(k): v for k, v in status_dist.items()},
        "error_count": len(error_entries)
    }

    # Write report
    write_summary_json(stats, output_file)
    print(f"Analysis complete. Summary saved to {output_file}")
    print(f"Total Entries: {stats['total_entries']}")
    print(f"Total Bytes: {stats['total_bytes_transferred']}")
    print(f"Error Count (>=400): {stats['error_count']}")

if __name__ == "__main__":
    main()
