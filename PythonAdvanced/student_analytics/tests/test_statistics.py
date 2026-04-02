import pytest
from src.models import Student
from src.services.statistics import GradeStatistics

def test_calculate_mean():
    assert GradeStatistics.calculate_mean([10.0, 20.0, 30.0]) == 20.0
    assert GradeStatistics.calculate_mean([]) == 0.0

def test_calculate_median():
    assert GradeStatistics.calculate_median([10.0, 30.0, 20.0]) == 20.0
    assert GradeStatistics.calculate_median([10.0, 20.0, 30.0, 40.0]) == 25.0

def test_calculate_mode():
    assert GradeStatistics.calculate_mode([10.0, 20.0, 20.0, 30.0]) == 20.0

def test_rolling_average():
    grades = [10.0, 20.0, 30.0, 40.0, 50.0]
    averages = GradeStatistics.rolling_average(grades, window_size=3)
    # 1: [10] -> 10
    # 2: [10, 20] -> 15
    # 3: [10, 20, 30] -> 20
    # 4: [20, 30, 40] -> 30
    # 5: [30, 40, 50] -> 40
    assert averages == [10.0, 15.0, 20.0, 30.0, 40.0]

def test_percentile_rankings():
    students = [
        Student(1, "Alice", "CS", 1, [90.0, 95.0]), # avg 92.5
        Student(2, "Bob", "Math", 1, [80.0, 80.0]), # avg 80.0
        Student(3, "Charlie", "Bio", 1, [70.0, 70.0]) # avg 70.0
    ]
    rankings = GradeStatistics.calculate_percentile_rankings(students)
    
    assert list(rankings.keys()) == ["Alice", "Bob", "Charlie"]
    assert rankings["Alice"]["percentile"] == 100.0
    assert rankings["Bob"]["percentile"] == 50.0  # 1 out of 2 trailing (Wait, total 3, rank 1 -> (3-1-1)/3 = 33.3? No, (3-1-1)/3 = 1/3 = 33.3. Let's precise: (3-1-1)/3 = 1/3 * 100 = 33.33)
    assert rankings["Charlie"]["percentile"] == 0.0
