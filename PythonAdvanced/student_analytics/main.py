import sys
from pathlib import Path
import json
from src.utils.file_handlers import yield_students_csv, write_report_json
from src.services.collections import GradeDistribution, StudentGrouper
from src.services.statistics import GradeStatistics
from src.models.types import ReportStructure

def main():
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    sample_csv = data_dir / "sample.csv"
    report_json = data_dir / "report.json"
    
    if not sample_csv.exists():
        sample_csv.write_text("id,name,major,year,grades\n1,Alice,CS,2023,\"90.0, 95.0\"\n2,Bob,Math,2023,\"80.0\"\n3,Charlie,CS,2023,\"70.0, 60.0\"\n4,Dave,Physics,2023,\"100.0, 90.0\"", encoding="utf-8")
        
    print(f"Reading students from: {sample_csv}")
    students = list(yield_students_csv(sample_csv))
    
    print(f"Processing statistics for {len(students)} students...")
    all_grades = []
    for s in students:
        all_grades.extend(s.grades)
        
    distribution = GradeDistribution(all_grades)
    grouper = StudentGrouper(students)
    ranked = GradeStatistics.calculate_percentile_rankings(students)
    
    report: ReportStructure = {
        "total_students": len(students),
        "overall_average": GradeStatistics.calculate_mean(all_grades),
        "grade_distribution": distribution.get_distribution(),
        "top_performers": [
            {"name": name, "average": data["average"], "percentile": data["percentile"]}
            for name, data in ranked.items()
        ],
        "major_groupings": {major: len(group) for major, group in grouper.group_by_major().items()}
    }
    
    write_report_json(report_json, report)
    print(f"Successfully wrote JSON report context to: {report_json}")
    print("\n--- FINAL REPORT ---")
    print(json.dumps(report, indent=4))
    
if __name__ == "__main__":
    main()
