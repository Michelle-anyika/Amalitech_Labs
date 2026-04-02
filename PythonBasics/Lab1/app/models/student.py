"""
Base Student class.
Demonstrates encapsulation, properties, magic methods, inheritance,
and email validation.
"""
import re
from datetime import date


class Student:
    """Base Student class with email validation."""

    def __init__(self, student_id: str, name: str, email: str, dob: date):
        self._student_id = student_id
        self._name = name
        self.dob = dob
        self.email = email  # will call the setter for validation
        self._enrolled_courses = []

    @property
    def student_id(self) -> str:
        return self._student_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> str:
        """Get student email."""
        return self._email

    @email.setter
    def email(self, value: str):
        """Set student email with validation."""
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, value):
            raise ValueError(f"Invalid email: {value}")
        self._email = value

    @property
    def enrolled_courses(self):
        return self._enrolled_courses

    def enroll(self, course):
        """Enroll student in a course (prevents duplicates)."""
        if course not in self._enrolled_courses:
            self._enrolled_courses.append(course)
            return True
        return False

    def get_student_type(self) -> str:
        """Polymorphic method to override in subclasses."""
        return "Regular Student"

    def __repr__(self) -> str:
        return f"Student(id={self._student_id}, name={self._name})"

    def __eq__(self, other) -> bool:
        if isinstance(other, Student):
            return self._student_id == other._student_id
        return False