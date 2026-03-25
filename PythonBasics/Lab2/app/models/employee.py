"""
Employee module containing base Employee class and role-specific subclasses.
Demonstrates inheritance, polymorphism, and property decorators.
"""

from abc import ABC, abstractmethod
from typing import Optional


class Employee(ABC):
    """Base abstract class for all employee types."""

    def __init__(self, emp_id: str, name: str, base_salary: float):
        self._emp_id = emp_id
        self._name = name
        self._base_salary = self._validate_salary(base_salary)
        self._bonus = 0.0
        self._tax_rate = 0.15

    @staticmethod
    def _validate_salary(salary: float) -> float:
        """Validate salary is positive."""
        if salary < 0:
            raise ValueError("Salary cannot be negative")
        return salary

    @property
    def emp_id(self) -> str:
        return self._emp_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def base_salary(self) -> float:
        return self._base_salary

    @base_salary.setter
    def base_salary(self, value: float):
        self._base_salary = self._validate_salary(value)

    @property
    def bonus(self) -> float:
        return self._bonus

    @bonus.setter
    def bonus(self, value: float):
        if value < 0:
            raise ValueError("Bonus cannot be negative")
        self._bonus = value

    @property
    def tax_rate(self) -> float:
        return self._tax_rate

    @tax_rate.setter
    def tax_rate(self, value: float):
        if not 0 <= value <= 1:
            raise ValueError("Tax rate must be between 0 and 1")
        self._tax_rate = value

    @abstractmethod
    def calculate_gross_pay(self) -> float:
        """Calculate gross pay before taxes."""
        pass

    def calculate_tax(self) -> float:
        """Calculate tax amount."""
        return self.calculate_gross_pay() * self._tax_rate

    def calculate_net_pay(self) -> float:
        """Calculate net pay after taxes."""
        return self.calculate_gross_pay() - self.calculate_tax()

    def generate_payslip(self) -> dict:
        """Generate payslip dictionary."""
        gross = self.calculate_gross_pay()
        tax = self.calculate_tax()
        net = self.calculate_net_pay()

        return {
            'emp_id': self._emp_id,
            'name': self._name,
            'role': self.__class__.__name__,
            'base_salary': self._base_salary,
            'bonus': self._bonus,
            'gross_pay': gross,
            'tax': tax,
            'net_pay': net
        }


class FullTimeEmployee(Employee):
    """Full-time employee with benefits and annual bonus."""

    def __init__(self, emp_id: str, name: str, base_salary: float, benefits: float = 0.0):
        super().__init__(emp_id, name, base_salary)
        self._benefits = benefits
        self._tax_rate = 0.20

    @property
    def benefits(self) -> float:
        return self._benefits

    @benefits.setter
    def benefits(self, value: float):
        if value < 0:
            raise ValueError("Benefits cannot be negative")
        self._benefits = value

    def calculate_gross_pay(self) -> float:
        """Gross pay includes base salary, bonus, and benefits."""
        return self._base_salary + self._bonus + self._benefits


class ContractEmployee(Employee):
    """Contract employee paid hourly."""

    def __init__(self, emp_id: str, name: str, hourly_rate: float, hours_worked: float = 0.0):
        super().__init__(emp_id, name, hourly_rate)
        self._hours_worked = hours_worked
        self._tax_rate = 0.10

    @property
    def hourly_rate(self) -> float:
        return self._base_salary

    @hourly_rate.setter
    def hourly_rate(self, value: float):
        self.base_salary = value

    @property
    def hours_worked(self) -> float:
        return self._hours_worked

    @hours_worked.setter
    def hours_worked(self, value: float):
        if value < 0:
            raise ValueError("Hours worked cannot be negative")
        self._hours_worked = value

    def calculate_gross_pay(self) -> float:
        """Gross pay based on hourly rate and hours worked."""
        return self._base_salary * self._hours_worked + self._bonus


class Intern(Employee):
    """Intern with stipend and minimal tax."""

    def __init__(self, emp_id: str, name: str, monthly_stipend: float):
        super().__init__(emp_id, name, monthly_stipend)
        self._tax_rate = 0.05

    @property
    def monthly_stipend(self) -> float:
        return self._base_salary

    @monthly_stipend.setter
    def monthly_stipend(self, value: float):
        self.base_salary = value

    def calculate_gross_pay(self) -> float:
        """Gross pay is monthly stipend plus any bonus."""
        return self._base_salary + self._bonus
