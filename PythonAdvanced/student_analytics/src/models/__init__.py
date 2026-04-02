from dataclasses import dataclass
from typing import List


@dataclass
class Student:
    id: int
    name: str
    major: str
    year: int
    grades: List[float]


@dataclass
class Course:
    id: str
    name: str
    credits: int

@dataclass
class Grade:
    student_id: int
    course_id: str
    score: float
    semester: int

