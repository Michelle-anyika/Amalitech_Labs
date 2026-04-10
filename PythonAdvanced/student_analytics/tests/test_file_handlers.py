import pytest
import json
from src.utils.file_handlers import read_students_csv, yield_students_csv, write_report_json

def test_file_handlers(tmp_path):
    csv_file = tmp_path / "students.csv"
    csv_file.write_text("id,name,major,year,grades\n1,Alice,CS,2023,\"90.0, 95.0\"\n2,Bob,Math,2023,", encoding="utf-8")
    
    # Test yield
    generator = yield_students_csv(csv_file)
    s1 = next(generator)
    assert s1.name == "Alice"
    assert s1.grades == [90.0, 95.0]
    
    # Test read full
    students = read_students_csv(csv_file)
    assert len(students) == 2
    assert students[1].name == "Bob"
    assert students[1].grades == []
    
    # Test JSON write
    json_file = tmp_path / "report.json"
    data = {"total": 2}
    write_report_json(json_file, data)
    assert json.loads(json_file.read_text(encoding="utf-8")) == {"total": 2}
        
def test_missing_files(tmp_path):
    with pytest.raises(FileNotFoundError):
        read_students_csv(tmp_path / "ghost.csv")
    with pytest.raises(FileNotFoundError):
        list(yield_students_csv(tmp_path / "ghost.csv"))
