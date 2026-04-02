"""
Graduate student class.
"""

from PythonBasics.Lab1 import Student

class Graduate(Student):
    """Graduate student class."""

    def __init__(self, student_id, name, email, research_area):
        super().__init__(student_id, name, email)
        self._research_area = research_area

    @property
    def research_area(self):
        return self._research_area

    def get_student_type(self):
        return f"Graduate ({self._research_area})"