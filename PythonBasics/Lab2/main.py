"""
Employee Payroll Tracker - Main Application
A comprehensive payroll management system demonstrating OOP principles,
inheritance, polymorphism, and modular design.
"""

from typing import List
from PythonBasics.Lab2.app.models.employee import Employee, FullTimeEmployee, ContractEmployee, Intern
from PythonBasics.Lab2.app.services.payroll_service import (
    print_payslip, print_summary_report, filter_employees_by_role,
    get_highest_paid_employee, format_currency
)
from PythonBasics.Lab2.data.data_loader import load_sample_employees, get_employee_by_id


def display_menu():
    """Display main menu options."""
    print("\n" + "="*50)
    print("EMPLOYEE PAYROLL TRACKER")
    print("="*50)
    print("1. View All Payslips")
    print("2. View Summary Report")
    print("3. View Payslip by Employee ID")
    print("4. View Employees by Role")
    print("5. Add New Employee")
    print("6. Update Employee Bonus")
    print("7. Exit")
    print("="*50)


def view_all_payslips(employees: List[Employee]):
    """Display all employee payslips."""
    for emp in employees:
        print_payslip(emp.generate_payslip())


def view_payslip_by_id(employees: List[Employee]):
    """View payslip for specific employee."""
    emp_id = input("Enter Employee ID: ").strip()
    try:
        emp = get_employee_by_id(employees, emp_id)
        print_payslip(emp.generate_payslip())
    except ValueError as e:
        print(f"Error: {e}")


def view_employees_by_role(employees: List[Employee]):
    """View employees filtered by role."""
    print("\nAvailable Roles:")
    print("1. FullTimeEmployee")
    print("2. ContractEmployee")
    print("3. Intern")

    choice = input("Select role (1-3): ").strip()
    role_map = {
        '1': 'FullTimeEmployee',
        '2': 'ContractEmployee',
        '3': 'Intern'
    }

    role = role_map.get(choice)
    if not role:
        print("Invalid choice")
        return

    filtered = filter_employees_by_role(employees, role)
    if not filtered:
        print(f"No employees found with role: {role}")
        return

    for emp in filtered:
        print_payslip(emp.generate_payslip())


def add_new_employee(employees: List[Employee]):
    """Add a new employee interactively."""
    print("\nSelect Employee Type:")
    print("1. Full-Time Employee")
    print("2. Contract Employee")
    print("3. Intern")

    choice = input("Enter choice (1-3): ").strip()

    try:
        emp_id = input("Employee ID: ").strip()
        name = input("Name: ").strip()

        if choice == '1':
            base_salary = float(input("Base Salary: "))
            benefits = float(input("Benefits: "))
            emp = FullTimeEmployee(emp_id, name, base_salary, benefits)
        elif choice == '2':
            hourly_rate = float(input("Hourly Rate: "))
            hours_worked = float(input("Hours Worked: "))
            emp = ContractEmployee(emp_id, name, hourly_rate, hours_worked)
        elif choice == '3':
            stipend = float(input("Monthly Stipend: "))
            emp = Intern(emp_id, name, stipend)
        else:
            print("Invalid choice")
            return

        bonus = input("Bonus (press Enter for 0): ").strip()
        if bonus:
            emp.bonus = float(bonus)

        employees.append(emp)
        print(f"\n✓ Employee {name} added successfully!")
        print_payslip(emp.generate_payslip())

    except ValueError as e:
        print(f"Error: {e}")


def update_employee_bonus(employees: List[Employee]):
    """Update bonus for an employee."""
    emp_id = input("Enter Employee ID: ").strip()
    try:
        emp = get_employee_by_id(employees, emp_id)
        print(f"\nCurrent bonus for {emp.name}: {format_currency(emp.bonus)}")
        new_bonus = float(input("Enter new bonus amount: "))
        emp.bonus = new_bonus
        print(f"✓ Bonus updated successfully!")
        print_payslip(emp.generate_payslip())
    except ValueError as e:
        print(f"Error: {e}")


def main():
    """Main application entry point."""
    print("\nInitializing Employee Payroll Tracker...")
    employees = load_sample_employees()
    print(f"✓ Loaded {len(employees)} employees")

    while True:
        display_menu()
        choice = input("\nEnter your choice (1-7): ").strip()

        if choice == '1':
            view_all_payslips(employees)
        elif choice == '2':
            print_summary_report(employees)
        elif choice == '3':
            view_payslip_by_id(employees)
        elif choice == '4':
            view_employees_by_role(employees)
        elif choice == '5':
            add_new_employee(employees)
        elif choice == '6':
            update_employee_bonus(employees)
        elif choice == '7':
            print("\nThank you for using Employee Payroll Tracker!")
            break
        else:
            print("\n Invalid choice. Please try again.")


if __name__ == '__main__':
    main()
