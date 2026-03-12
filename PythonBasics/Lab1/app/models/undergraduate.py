"""
Undergraduate student class.
"""

from PythonBasics.Lab1.app.models.student import Student

class Undergraduate(Student):
    """Undergraduate student class."""

    def __init__(self, student_id, name, email, year):
        super().__init__(student_id, name, email)
        self._year = year

    @property
    def year(self):
        return self._year

    def get_student_type(self):
        return f"Undergraduate (Year {self._year})"