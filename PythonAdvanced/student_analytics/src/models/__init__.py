from dataclasses import dataclass
from typing import List


@dataclass
class Student:
    id: int
    name: str
    major: str
    year: int
    grades: List[float]
