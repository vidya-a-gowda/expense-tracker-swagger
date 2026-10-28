# Expense Tracker API

A lightweight FastAPI backend for tracking personal expenses, filtering records, and viewing summary analytics.

## Features

- Create, read, update, and delete expense records
- Filter expenses by category and date range
- View total spending and category breakdown
- Identify the highest expense entry
- Persistent SQLite storage via SQLAlchemy

## Tech Stack

- Python 3
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic

## Project Structure

```text
expense-tracker-api-python/
├── api/
│   └── routes/
│       └── expenses.py
├── crud/
│   └── expense.py
├── db/
│   └── database.py
├── models/
│   └── expense.py
├── schemas/
│   └── expense.py
├── main.py
├── .gitignore
├── expenses.db
└── README.md
```

## Setup

1. Create and activate a virtual environment:

```bash
cd /path/to/expense-tracker-api-python
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install fastapi uvicorn sqlalchemy pydantic
```

## Run the Application

From the project root:

```bash
PYTHONPATH=. python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at:

- http://127.0.0.1:8000
- Swagger docs: http://127.0.0.1:8000/docs

## API Endpoints

### Expenses

- `POST /expenses/` - Create a new expense
- `GET /expenses/` - List all expenses with optional filters
  - `category` (optional)
  - `start_date` (optional)
  - `end_date` (optional)
- `GET /expenses/{expense_id}` - Fetch one expense by ID
- `PUT /expenses/{expense_id}` - Update an expense by ID
- `DELETE /expenses/{expense_id}` - Delete an expense by ID

### Analytics

- `GET /expenses/summary` - Return total spend, category totals, and highest expense

## Example Request

Create an expense:

```bash
curl -X POST "http://127.0.0.1:8000/expenses/" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 45.50,
    "category": "Food",
    "description": "Lunch groceries",
    "date": "2026-10-28"
  }'
```

## Database

The app uses a SQLite database file named `expenses.db` stored in the project root.

## Notes

- The app creates database tables automatically on startup via `Base.metadata.create_all(bind=engine)` in `main.py`.
- If you are running from a different environment, ensure the project root is on `PYTHONPATH` so the local packages resolve correctly.
