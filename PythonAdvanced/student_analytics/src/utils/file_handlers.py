import csv
import json
from pathlib import Path
from typing import List, Any, Union, Iterator

from src.models import Student
from src.models.types import FlexiblePath

def parse_student_row(row: dict) -> Student:
    grades_str = row.get('grades', '')
    grades = [float(g.strip()) for g in grades_str.split(',')] if grades_str else []
    return Student(
        id=int(row['id']),
        name=row['name'],
        major=row['major'],
        year=int(row['year']),
        grades=grades
    )

def read_students_csv(file_path: FlexiblePath) -> List[Student]:
    """Reads a CSV file and loads the dataset into memory."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
        
    students = []
    with path.open('r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            students.append(parse_student_row(row))
    return students

def yield_students_csv(file_path: FlexiblePath) -> Iterator[Student]:
    """Memory-efficient generator approach to loading students."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
        
    with path.open('r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield parse_student_row(row)

def write_report_json(file_path: FlexiblePath, data: Any) -> None:
    """Writes report dictionary to JSON with context manager."""
    path = Path(file_path)
    with path.open('w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
