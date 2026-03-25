"""
Course model.
Handles course info and enrolled students.
"""

class Course:
    """Represents a course."""

    def __init__(self, course_id, name):
        self._course_id = course_id
        self._name = name
        self._students = {}  # {student: grade}

    @property
    def course_id(self):
        return self._course_id

    @property
    def name(self):
        return self._name

    @property
    def students(self):
        return self._students

    def add_student(self, student, grade=0):
        """Add a student with optional grade."""
        self._students[student] = grade

    def set_grade(self, student, grade):
        """Set grade for a student."""
        if student in self._students:
            self._students[student] = grade

    def average_grade(self):
        """Compute average grade."""
        if not self._students:
            return 0
        return sum(self._students.values()) / len(self._students)

    def __repr__(self):
        return f"Course(id={self._course_id}, name={self._name})"