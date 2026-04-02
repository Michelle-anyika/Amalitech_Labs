"""
Service for managing courses.
"""

from PythonBasics.Lab1.import Course

courses = {}  # {course_id: Course instance}

def add_course(course_id, name):
    """Add a course."""
    course = Course(course_id, name)
    courses[course_id] = course
    return course

def get_course(course_id):
    return courses.get(course_id)

def list_courses():
    return list(courses.values())