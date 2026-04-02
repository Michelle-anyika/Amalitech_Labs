"""
Course report implementation using logging.
"""

import logging
from PythonBasics.Lab1 import Report

logging.basicConfig(level=logging.INFO, format="%(message)s")

class CourseReport(Report):
    """Generate course reports."""

    def __init__(self, course):
        self.course = course

    def generate(self):
        logging.info(f"\nCourse Report: {self.course.name}")
        for student, grade in self.course.students.items():
            logging.info(f"{student.name} ({student.get_student_type()}) - Grade: {grade}")
        logging.info(f"Average Grade: {self.course.average_grade():.2f}")