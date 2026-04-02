"""
Service for handling enrollments.
"""

from PythonBasics.Lab1 import Enrollment

def enroll_student(student, course):
    """Enroll a student in a course."""
    enrollment = Enrollment(student, course)
    enrollment.enroll()