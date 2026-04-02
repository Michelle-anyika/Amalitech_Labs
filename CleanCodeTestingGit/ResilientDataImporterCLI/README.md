# Resilient Data Importer CLI

##  Overview
A Python CLI tool that imports user data from CSV files into a JSON database with robust error handling, validation, and logging.

---

##  Features
- CSV parsing
- Data validation
- Duplicate detection
- Custom exception handling
- Structured logging
- JSON-based storage
- Full pytest test suite
- CI/CD pipeline (GitHub Actions)

---

##  Setup

```bash
git clone <repo-url>
cd Resilient-Data-Importer-CLI

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
pre-commit install