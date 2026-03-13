# Employee Payroll Tracker

A comprehensive payroll management system demonstrating Python OOP principles, inheritance, polymorphism, and modular design.

## Features

- **Multiple Employee Types**: Full-time, Contract, and Intern employees
- **Polymorphic Design**: Unified interface for different employee types
- **Property Decorators**: Safe data access and validation
- **Interactive CLI**: Menu-driven interface
- **Comprehensive Testing**: Full test coverage with pytest

## Setup

### Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

### Run Application
```bash
python main.py
```

### Run Tests
```bash
pytest test_payroll.py -v
```

## Architecture

- `employee.py` - Employee classes with inheritance
- `payroll.py` - Payroll computation functions
- `data.py` - Data management utilities
- `main.py` - CLI application
- `test_payroll.py` - Test suite
