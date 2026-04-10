# C:\Users\Amalitech\Desktop\Amalitech\Amalitech_Labs\PythonAdvanced\student_analytics\tests\test_collections.py

import pytest
from src.models import Student, Grade
from src.services import GradeDistribution, StudentGrouper


def test_grade_distribution_counter():
    """Test grade distribution using Counter - RED phase"""
    grades = [85.0, 90.0, 85.0, 78.0, 92.0, 85.0, 88.0]
    dist = GradeDistribution(grades)

    # Counter should count frequency of each grade
    assert dist.get_distribution() == {85.0: 3, 90.0: 1, 78.0: 1, 92.0: 1, 88.0: 1}
    assert dist.most_common(1) == [(85.0, 3)]  # Grade 85.0 appears 3 times
    assert dist.total_grades() == 7


def test_student_grouper_defaultdict():
    """Test grouping students by major using defaultdict - RED phase"""
    students = [
        Student(1, "Alice", "CS", 2023, [85.0, 90.0]),
        Student(2, "Bob", "CS", 2023, [92.0, 88.0]),
        Student(3, "Charlie", "Math", 2023, [78.0, 82.0]),
    ]

    grouper = StudentGrouper(students)
    groups = grouper.group_by_major()

    assert len(groups["CS"]) == 2
    assert len(groups["Math"]) == 1
    assert groups["CS"][0].name == "Alice"
