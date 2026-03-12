"""
CLI for Student Course Management System.
Includes input validation, logging, and error handling.
"""

from app.services.student_service import add_student, get_student, list_students
from app.services.course_service import add_course, get_course, list_courses
from app.services.enrollment_service import enroll_student
from app.reports.course_report import CourseReport
from app.utils.helpers import print_separator

def menu():
    """Main CLI menu."""
    while True:
        print_separator()
        print("Student Course Management System")
        print("1. Add Student")
        print("2. Add Course")
        print("3. Enroll Student")
        print("4. View Students")
        print("5. View Courses")
        print("6. Generate Course Report")
        print("7. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            sid = input("Student ID: ").strip()
            name = input("Name: ").strip()
            email = input("Email: ").strip()
            stype = input("Type (undergraduate/graduate): ").strip().lower()

            try:
                if stype == "undergraduate":
                    year = int(input("Year: "))
                    add_student(sid, name, email, stype, year)
                elif stype == "graduate":
                    research = input("Research Area: ").strip()
                    add_student(sid, name, email, stype, research)
                else:
                    print("Invalid student type")
            except ValueError:
                print("Invalid input, try again")

        elif choice == "2":
            cid = input("Course ID: ").strip()
            cname = input("Course Name: ").strip()
            add_course(cid, cname)

        elif choice == "3":
            sid = input("Student ID: ").strip()
            cid = input("Course ID: ").strip()

            student = get_student(sid)
            course = get_course(cid)

            if student and course:
                enroll_student(student, course)
                try:
                    grade = float(input("Enter grade (0-100): "))
                    if 0 <= grade <= 100:
                        course.set_grade(student, grade)
                    else:
                        print("Grade must be 0-100")
                except ValueError:
                    print("Invalid grade input")
            else:
                print("Student or course not found")

        elif choice == "4":
            for s in list_students():
                print(s)

        elif choice == "5":
            for c in list_courses():
                print(c)

        elif choice == "6":
            cid = input("Course ID: ").strip()
            course = get_course(cid)
            if course:
                report = CourseReport(course)
                report.generate()
            else:
                print("Course not found")

        elif choice == "7":
            print("Exiting...")
            break

        else:
            print("Invalid choice, try again")

if __name__ == "__main__":
    menu()