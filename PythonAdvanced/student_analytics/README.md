# Student Grade Analytics Tool

A robust backend analytics tool written to perform data processing, statistical derivations, and reporting using Python's advanced collections natively and elegantly.

## Setup Instructions
1. Install Python 3.11+.
2. Install the necessary dependencies: `pip install -r requirements.txt`.
3. Run the existing tests using `python -m pytest`.

## Features
- **Generators & File Handlers**: Parses and interprets dynamically CSV rows via a `yield` generator to preserve memory footprint on large datasets.
- **`defaultdict` & `Counter`**: Used aggressively in `GradeDistribution` and `StudentGrouper` to effortlessly pivot datasets by Major, Year, or grade distribution bins without heavy nested loops.
- **`deque` from `collections`**: Uses sliding window structures to determine the user's `rolling_average` over numerous semesters without the heavy slicing overhead that typical lists mandate.
- **`OrderedDict`**: Guarantees output layout insertion ordering so JSON reports are reliably constructed in high-to-low percentile configurations.

## Performance considerations vs Native Types
| Collection Method | Native Equivalent | Memory / Compute Benefit |
|-------------------|-------------------|--------------------------|
| `collections.deque(maxlen=N)` | `list.append()` + `list.pop(0)` | `O(1)` runtime operations on edges instead of `O(n)` lists memory shifting offsets. |
| `collections.Counter` | `dict` insertions inside `if` statments | Built-in C-optimized iteration and `most_common()` binary heap mapping allows for immediate frequency counts. |
| `yield` function generator | returning monolithic `List[Student]` array | Substantially reduces RAM threshold issues by pulling instances row-by-row on extreme datasets (>1GB bounds). |

## Sample JSON Report Output
```json
{
    "total_students": 3,
    "overall_average": 82.5,
    "grade_distribution": {"95.0": 1, "90.0": 1, "80.0": 2, "70.0": 2},
    "top_performers": [
        {
            "name": "Alice",
            "average": 92.5,
            "percentile": 100.0
        }
    ],
    "major_groupings": {
        "CS": 1,
        "Math": 1,
        "Bio": 1
    }
}
```
