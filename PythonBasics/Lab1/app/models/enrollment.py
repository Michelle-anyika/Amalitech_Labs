"""
Enrollment logic linking students and courses.
"""

class Enrollment:
    """Handles enrollment operations."""

    def __init__(self, student, course):
        self.student = student
        self.course = course

    def enroll(self):
        """Enroll student in course."""
        self.student.enroll(self.course)
        self.course.add_student(self.student)