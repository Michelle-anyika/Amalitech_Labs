import pytest
from src.models import Student


def test_student_creation():
    student = Student(id=1, name="John Doe", major="Computer Science", year=2023, grades=[85.0, 90.0])
    assert student.id == 1
    assert student.name == "John Doe"
    assert student.major == "Computer Science"
    assert student.year == 2023
    assert student.grades == [85.0, 90.0]
