"""
Data module for loading and managing employee data.
Demonstrates use of lists and dictionaries for data organization.
"""

from typing import List, Dict
from PythonBasics.Lab2.app.models.employee import Employee, FullTimeEmployee, ContractEmployee, Intern


def load_sample_employees() -> List[Employee]:
    """Load sample employee data."""
    employees = [
        FullTimeEmployee("FT001", "Alice Johnson", 75000, benefits=5000),
        FullTimeEmployee("FT002", "Bob Smith", 85000, benefits=6000),
        ContractEmployee("CT001", "Charlie Brown", 50, hours_worked=160),
        ContractEmployee("CT002", "Diana Prince", 65, hours_worked=140),
        Intern("IN001", "Eve Davis", 2000),
        Intern("IN002", "Frank Miller", 2500),
    ]

    # Add bonuses using property setters
    employees[0].bonus = 5000
    employees[1].bonus = 7000
    employees[2].bonus = 1000

    return employees


def create_employee_from_dict(data: Dict) -> Employee:
    """Create employee instance from dictionary data."""
    role = data.get('role', '').lower()

    if role == 'fulltime':
        emp = FullTimeEmployee(
            data['emp_id'],
            data['name'],
            data['base_salary'],
            data.get('benefits', 0.0)
        )
    elif role == 'contract':
        emp = ContractEmployee(
            data['emp_id'],
            data['name'],
            data['hourly_rate'],
            data.get('hours_worked', 0.0)
        )
    elif role == 'intern':
        emp = Intern(
            data['emp_id'],
            data['name'],
            data['monthly_stipend']
        )
    else:
        raise ValueError(f"Unknown role: {role}")

    if 'bonus' in data:
        emp.bonus = data['bonus']

    return emp


def export_employees_to_dict(employees: List[Employee]) -> List[Dict]:
    """Export employees to list of dictionaries."""
    return [
        {
            'emp_id': emp.emp_id,
            'name': emp.name,
            'role': emp.__class__.__name__,
            'base_salary': emp.base_salary,
            'bonus': emp.bonus,
            'tax_rate': emp.tax_rate
        }
        for emp in employees
    ]


def get_employee_by_id(employees: List[Employee], emp_id: str) -> Employee:
    """Find employee by ID."""
    for emp in employees:
        if emp.emp_id == emp_id:
            return emp
    raise ValueError(f"Employee with ID {emp_id} not found")


def get_employees_above_salary(employees: List[Employee], threshold: float) -> List[Employee]:
    """Get employees with net pay above threshold."""
    return [emp for emp in employees if emp.calculate_net_pay() > threshold]
