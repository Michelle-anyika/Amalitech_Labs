"""
Payroll module for salary computations and payroll management.
Contains reusable functions for payroll operations.
"""

from typing import List, Dict
from PythonBasics.Lab2.app.models.employee import Employee


def calculate_total_payroll(employees: List[Employee]) -> float:
    """Calculate total payroll cost for all employees."""
    return sum(emp.calculate_net_pay() for emp in employees)


def calculate_total_tax(employees: List[Employee]) -> float:
    """Calculate total tax collected from all employees."""
    return sum(emp.calculate_tax() for emp in employees)


def generate_payroll_report(employees: List[Employee]) -> List[Dict]:
    """Generate payroll report for all employees."""
    return [emp.generate_payslip() for emp in employees]


def filter_employees_by_role(employees: List[Employee], role: str) -> List[Employee]:
    """Filter employees by role type."""
    return [emp for emp in employees if emp.__class__.__name__ == role]


def get_highest_paid_employee(employees: List[Employee]) -> Employee:
    """Get the highest paid employee by net pay."""
    if not employees:
        raise ValueError("Employee list is empty")
    return max(employees, key=lambda emp: emp.calculate_net_pay())


def format_currency(amount: float) -> str:
    """Format amount as currency."""
    return f"${amount:,.2f}"


def print_payslip(payslip: Dict) -> None:
    """Print formatted payslip."""
    print("\n" + "="*50)
    print(f"PAYSLIP - {payslip['role'].upper()}")
    print("="*50)
    print(f"Employee ID:    {payslip['emp_id']}")
    print(f"Name:           {payslip['name']}")
    print(f"Base Salary:    {format_currency(payslip['base_salary'])}")
    print(f"Bonus:          {format_currency(payslip['bonus'])}")
    print(f"Gross Pay:      {format_currency(payslip['gross_pay'])}")
    print(f"Tax:            {format_currency(payslip['tax'])}")
    print(f"Net Pay:        {format_currency(payslip['net_pay'])}")
    print("="*50)


def print_summary_report(employees: List[Employee]) -> None:
    """Print summary payroll report."""
    print("\n" + "="*50)
    print("PAYROLL SUMMARY REPORT")
    print("="*50)
    print(f"Total Employees:    {len(employees)}")
    print(f"Total Payroll:      {format_currency(calculate_total_payroll(employees))}")
    print(f"Total Tax:          {format_currency(calculate_total_tax(employees))}")

    # Role breakdown
    roles = set(emp.__class__.__name__ for emp in employees)
    print("\nBreakdown by Role:")
    for role in sorted(roles):
        role_employees = filter_employees_by_role(employees, role)
        role_payroll = sum(emp.calculate_net_pay() for emp in role_employees)
        print(f"  {role}: {len(role_employees)} employees - {format_currency(role_payroll)}")

    if employees:
        highest_paid = get_highest_paid_employee(employees)
        print(f"\nHighest Paid: {highest_paid.name} ({highest_paid.__class__.__name__}) - "
              f"{format_currency(highest_paid.calculate_net_pay())}")
    print("="*50)
