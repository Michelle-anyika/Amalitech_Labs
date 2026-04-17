# DatabaseFundamental - Multi-Lab Structure

This repository contains multiple database fundamentals labs. Each lab is self-contained with its own dependencies, Docker setup, and tests.

## 📚 Labs Overview

### Lab 1: E-Commerce Analytics Data Pipeline ✅
**Status**: Complete
**Location**: `Lab1_EcommerceAnalytics/`

An end-to-end data pipeline for an e-commerce platform featuring:
- PostgreSQL with normalized 3NF schema
- Redis caching layer
- MongoDB for session management
- Complex SQL analytics (window functions, CTEs)
- Query optimization (3-10x performance improvements)
- 40+ unit tests

**Quick Start**:
```bash
cd Lab1_EcommerceAnalytics
docker-compose up -d
pip install -r requirements.txt
python src/scripts/populate_db.py
pytest tests/ -v
```

See `Lab1_EcommerceAnalytics/README.md` for detailed documentation.

---

### Lab 2: Coming Soon
**Status**: Planned
**Location**: `Lab2_*/`

---

### Lab 3: Coming Soon
**Status**: Planned
**Location**: `Lab3_*/`

---

## 🗂️ Project Structure

```
DatabaseFundamental/
├── README.md                          ← This file
├── Lab1_EcommerceAnalytics/           ← Lab 1 (Self-contained)
│   ├── README.md
│   ├── QUICK_START.md
│   ├── requirements.txt
│   ├── docker-compose.yml
│   ├── .env.example
│   ├── .gitignore
│   ├── __init__.py
│   ├── src/
│   │   ├── config/
│   │   ├── db/
│   │   ├── models/
│   │   ├── operations/
│   │   ├── utils/
│   │   └── scripts/
│   ├── sql/
│   ├── mongo/
│   ├── tests/
│   └── docs/
│
├── Lab2_*/                            ← Lab 2 (Coming soon)
│
└── Lab3_*/                            ← Lab 3 (Coming soon)
```

---

## 🚀 Running Individual Labs

Each lab is completely independent. Navigate to the lab folder and follow its README:

```bash
# Lab 1
cd Lab1_EcommerceAnalytics
docker-compose up -d
# ... follow Lab1_EcommerceAnalytics/README.md

# Lab 2 (when ready)
cd Lab2_*
docker-compose up -d

# Lab 3 (when ready)
cd Lab3_*
docker-compose up -d
```

---

## 📋 Requirements

- Python 3.11+
- Docker & Docker Compose
- Git

---

## 📝 Documentation

Each lab has its own documentation:
- `README.md` - Overview and setup
- `QUICK_START.md` - Quick reference guide
- `docs/` - Detailed documentation

---

## ✅ Branch Information

All labs are developed on separate feature branches:
- Lab 1: `lab1-ecommerce-analytics-pipeline`
- Lab 2: (To be created)
- Lab 3: (To be created)

---

## 🎓 Learning Path

1. **Lab 1: E-Commerce Analytics** (Database Design, CRUD, NoSQL, Analytics)
   - Master relational database design
   - Learn transactional integrity
   - Explore NoSQL integration
   - Optimize query performance

2. **Lab 2**: (Coming soon)

3. **Lab 3**: (Coming soon)

---

## 🤝 Contributing

When adding Lab 2 or Lab 3:
1. Create new folder: `Lab2_*/` or `Lab3_*/`
2. Follow the same structure as Lab 1
3. Include all necessary files (requirements.txt, docker-compose.yml, etc.)
4. Create comprehensive README
5. Add tests

---

## 📞 Support

For each lab, refer to:
- `[LabX]/README.md` - Main documentation
- `[LabX]/QUICK_START.md` - Setup guide
- `[LabX]/docs/` - Detailed explanations
- `[LabX]/tests/` - Usage examples

---

**Last Updated**: April 6, 2026

