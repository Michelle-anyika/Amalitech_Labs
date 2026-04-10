from typing import TypedDict, List, Dict, Optional, Union
from pathlib import Path
from . import Student, Grade

StudentList = List[Student]
MajorGroups = Dict[str, List[Student]]
FlexiblePath = Union[str, Path]
OptionalGrade = Optional[Grade]

class ReportStructure(TypedDict):
    total_students: int
    overall_average: float
    grade_distribution: Dict[float, int]
    top_performers: List[Dict[str, Union[str, float]]]
    major_groupings: Dict[str, int]
