import unittest
from PythonBasics.Lab1.app.models.student import Student
from PythonBasics.Lab1.app.models.undergraduate import Undergraduate
from PythonBasics.Lab1.app.models.graduate import Graduate

class TestStudents(unittest.TestCase):

    def test_undergraduate_creation(self):
        u = Undergraduate("1", "Alice", "alice@mail.com", 2)
        self.assertEqual(u.get_student_type(), "Undergraduate (Year 2)")

    def test_graduate_creation(self):
        g = Graduate("2", "Bob", "bob@mail.com", "AI")
        self.assertEqual(g.get_student_type(), "Graduate (AI)")

    def test_student_enroll(self):
        s = Student("3", "Charlie", "c@mail.com")
        self.assertTrue(s.enroll("Python"))
        self.assertFalse(s.enroll("Python"))  # duplicate

if __name__ == "__main__":
    unittest.main()