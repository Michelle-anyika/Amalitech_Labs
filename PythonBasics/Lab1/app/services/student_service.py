"""
Service for managing students.
"""

from PythonBasics.Lab1.app.models.undergraduate import Undergraduate
from PythonBasics.Lab1.app.models.graduate import Graduate

students = {}  # {student_id: Student instance}

def add_student(student_id, name, email, student_type, *args):
    """Add a student to the system."""
    if student_type == "undergraduate":
        student = Undergraduate(student_id, name, email, *args)
    elif student_type == "graduate":
        student = Graduate(student_id, name, email, *args)
    else:
        raise ValueError("Invalid student type")

    students[student_id] = student
    return student

def get_student(student_id):
    return students.get(student_id)

def list_students():
    return list(students.values())