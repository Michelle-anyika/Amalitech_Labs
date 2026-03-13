"""Basic tests for payroll system."""

"""
Test suite for Employee Payroll Tracker.
Demonstrates testing, debugging, and validation.
"""
import pytest
from PythonBasics.Lab2.app.models.employee import Employee, FullTimeEmployee, ContractEmployee, Intern
from PythonBasics.Lab2.app.services.payroll_service import (
    calculate_total_payroll, calculate_total_tax,
    filter_employees_by_role, get_highest_paid_employee
)
from PythonBasics.Lab2.data.data_loader import load_sample_employees, create_employee_from_dict


class TestEmployee:
    """Test cases for Employee classes."""

    def test_fulltime_employee_creation(self):
        emp = FullTimeEmployee("FT001", "John Doe", 80000, 5000)
        assert emp.emp_id == "FT001"
        assert emp.name == "John Doe"
        assert emp.base_salary == 80000
        assert emp.benefits == 5000

    def test_fulltime_gross_pay(self):
        emp = FullTimeEmployee("FT001", "John Doe", 80000, 5000)
        emp.bonus = 10000
        assert emp.calculate_gross_pay() == 95000

    def test_fulltime_tax_calculation(self):
        emp = FullTimeEmployee("FT001", "John Doe", 80000, 5000)
        assert emp.calculate_tax() == 17000  # 20% of 85000

    def test_contract_employee_creation(self):
        emp = ContractEmployee("CT001", "Jane Smith", 50, 160)
        assert emp.hourly_rate == 50
        assert emp.hours_worked == 160

    def test_contract_gross_pay(self):
        emp = ContractEmployee("CT001", "Jane Smith", 50, 160)
        assert emp.calculate_gross_pay() == 8000

    def test_intern_creation(self):
        emp = Intern("IN001", "Bob Junior", 2000)
        assert emp.monthly_stipend == 2000
        assert emp.tax_rate == 0.05

    def test_negative_salary_raises_error(self):
        with pytest.raises(ValueError):
            FullTimeEmployee("FT001", "Test", -1000, 0)

    def test_negative_bonus_raises_error(self):
        emp = FullTimeEmployee("FT001", "Test", 50000, 0)
        with pytest.raises(ValueError):
            emp.bonus = -500

    def test_invalid_tax_rate_raises_error(self):
        emp = FullTimeEmployee("FT001", "Test", 50000, 0)
        with pytest.raises(ValueError):
            emp.tax_rate = 1.5

    def test_property_setters(self):
        emp = FullTimeEmployee("FT001", "Test", 50000, 2000)
        emp.base_salary = 60000
        emp.bonus = 5000
        emp.benefits = 3000
        assert emp.base_salary == 60000
        assert emp.bonus == 5000
        assert emp.benefits == 3000

    def test_payslip_generation(self):
        emp = FullTimeEmployee("FT001", "Test", 50000, 2000)
        payslip = emp.generate_payslip()
        assert payslip['emp_id'] == "FT001"
        assert payslip['name'] == "Test"
        assert payslip['role'] == "FullTimeEmployee"
        assert 'gross_pay' in payslip
        assert 'net_pay' in payslip


class TestPayroll:
    """Test cases for payroll functions."""

    def test_calculate_total_payroll(self):
        employees = [
            FullTimeEmployee("FT001", "Alice", 50000, 2000),
            ContractEmployee("CT001", "Bob", 50, 100)
        ]
        total = calculate_total_payroll(employees)
        assert total > 0

    def test_calculate_total_tax(self):
        employees = [
            FullTimeEmployee("FT001", "Alice", 50000, 2000)
        ]
        tax = calculate_total_tax(employees)
        assert tax == 10400  # 20% of 52000

    def test_filter_employees_by_role(self):
        employees = load_sample_employees()
        fulltime = filter_employees_by_role(employees, "FullTimeEmployee")
        assert all(isinstance(emp, FullTimeEmployee) for emp in fulltime)

    def test_get_highest_paid_employee(self):
        employees = [
            FullTimeEmployee("FT001", "Alice", 50000, 0),
            FullTimeEmployee("FT002", "Bob", 80000, 0)
        ]
        highest = get_highest_paid_employee(employees)
        assert highest.name == "Bob"

    def test_empty_employee_list_raises_error(self):
        with pytest.raises(ValueError):
            get_highest_paid_employee([])


class TestData:
    """Test cases for data module."""

    def test_load_sample_employees(self):
        employees = load_sample_employees()
        assert len(employees) > 0
        assert any(isinstance(emp, FullTimeEmployee) for emp in employees)
        assert any(isinstance(emp, ContractEmployee) for emp in employees)
        assert any(isinstance(emp, Intern) for emp in employees)

    def test_create_employee_from_dict_fulltime(self):
        data = {
            'role': 'fulltime',
            'emp_id': 'FT001',
            'name': 'Test',
            'base_salary': 50000,
            'benefits': 2000,
            'bonus': 5000
        }
        emp = create_employee_from_dict(data)
        assert isinstance(emp, FullTimeEmployee)
        assert emp.bonus == 5000

    def test_create_employee_from_dict_contract(self):
        data = {
            'role': 'contract',
            'emp_id': 'CT001',
            'name': 'Test',
            'hourly_rate': 50,
            'hours_worked': 160
        }
        emp = create_employee_from_dict(data)
        assert isinstance(emp, ContractEmployee)

    def test_create_employee_invalid_role(self):
        data = {
            'role': 'invalid',
            'emp_id': 'XX001',
            'name': 'Test'
        }
        with pytest.raises(ValueError):
            create_employee_from_dict(data)


class TestPolymorphism:
    """Test polymorphic behavior across employee types."""

    def test_polymorphic_gross_pay_calculation(self):
        employees = [
            FullTimeEmployee("FT001", "Alice", 60000, 3000),
            ContractEmployee("CT001", "Bob", 50, 160),
            Intern("IN001", "Charlie", 2000)
        ]

        # All employees can calculate gross pay polymorphically
        gross_pays = [emp.calculate_gross_pay() for emp in employees]
        assert len(gross_pays) == 3
        assert all(pay > 0 for pay in gross_pays)

    def test_polymorphic_payslip_generation(self):
        employees = [
            FullTimeEmployee("FT001", "Alice", 60000, 3000),
            ContractEmployee("CT001", "Bob", 50, 160),
            Intern("IN001", "Charlie", 2000)
        ]

        # All employees can generate payslips polymorphically
        payslips = [emp.generate_payslip() for emp in employees]
        assert len(payslips) == 3
        assert all('net_pay' in slip for slip in payslips)
