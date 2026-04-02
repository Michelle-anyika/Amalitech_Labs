from collections import Counter, defaultdict
from typing import List, Dict, Tuple
from src.models import Student

class GradeDistribution:
    def __init__(self, grades: List[float]):
        self._distribution = Counter(grades)
        
    def get_distribution(self) -> Dict[float, int]:
        return dict(self._distribution)
        
    def most_common(self, n: int) -> List[Tuple[float, int]]:
        return self._distribution.most_common(n)
        
    def total_grades(self) -> int:
        return sum(self._distribution.values())

class StudentGrouper:
    def __init__(self, students: List[Student]):
        self.students = students
        
    def group_by_major(self) -> Dict[str, List[Student]]:
        groups = defaultdict(list)
        for student in self.students:
            groups[student.major].append(student)
        return groups
