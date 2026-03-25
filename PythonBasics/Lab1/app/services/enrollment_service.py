"""
Service for handling enrollments.
"""

from PythonBasics.Lab1.app.models.enrollment import Enrollment

def enroll_student(student, course):
    """Enroll a student in a course."""
    enrollment = Enrollment(student, course)
    enrollment.enroll()