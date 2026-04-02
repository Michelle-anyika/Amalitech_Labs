import pytest
from src.models import Student


def test_student_creation():
    student = Student(id=1, name="John Doe", major="Computer Science", year=2023, grades=[85.0, 90.0])
    assert student.id == 1
    assert student.name == "John Doe"
    assert student.major == "Computer Science"
    assert student.year == 2023
    assert student.grades == [85.0, 90.0]


def test_course_creation():
    from src.models import Course
    course = Course(id="CS101", name="Introduction to Computer Science", credits=3)
    assert course.id == "CS101"
    assert course.name == "Introduction to Computer Science"
    assert course.credits == 3


def test_grade_creation():
    """Test case for Grade model"""
    from src.models import Grade
    grade = Grade(student_id=1, course_id="CS101", score=85.5, semester=1)
    assert grade.student_id == 1
    assert grade.course_id == "CS101"
    assert grade.score == 85.5
    assert grade.semester == 1
