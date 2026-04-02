from collections import deque, Counter, OrderedDict
from typing import List, Dict, Tuple, Iterator
from src.models import Student

class GradeStatistics:
    @staticmethod
    def calculate_mean(grades: List[float]) -> float:
        if not grades:
            return 0.0
        return sum(grades) / len(grades)

    @staticmethod
    def calculate_median(grades: List[float]) -> float:
        if not grades:
            return 0.0
        sorted_grades = sorted(grades)
        n = len(sorted_grades)
        mid = n // 2
        if n % 2 == 0:
            return (sorted_grades[mid - 1] + sorted_grades[mid]) / 2
        return sorted_grades[mid]

    @staticmethod
    def calculate_mode(grades: List[float]) -> float:
        if not grades:
            return 0.0
        # Use Counter to get the single most common grade
        return Counter(grades).most_common(1)[0][0]
        
    @staticmethod
    def rolling_average(grades: List[float], window_size: int = 3) -> List[float]:
        """Track grade trends over semesters using deque."""
        if not grades:
            return []
        
        window = deque(maxlen=window_size)
        rolling_averages = []
        
        for grade in grades:
            window.append(grade)
            rolling_averages.append(sum(window) / len(window))
            
        return rolling_averages

    @staticmethod
    def calculate_percentile_rankings(students: List[Student]) -> OrderedDict:
        """Calculate percentiles and store them in an OrderedDict, sorted highest to lowest."""
        # Calculate averages for each student
        averages = {s.id: GradeStatistics.calculate_mean(s.grades) for s in students}
        
        # Sort student ids by average descending
        sorted_ids = sorted(averages.keys(), key=lambda x: averages[x], reverse=True)
        total_students = len(sorted_ids)
        
        rankings = OrderedDict()
        for rank, student_id in enumerate(sorted_ids):
            # Percentile formula
            percentile = ((total_students - rank - 1) / (total_students - 1)) * 100 if total_students > 1 else 100.0
            
            # Find the student object dynamically using a generator expression
            student = next(s for s in students if s.id == student_id)
            
            rankings[student.name] = {
                "average": averages[student_id],
                "percentile": round(percentile, 2)
            }
            
        return rankings
