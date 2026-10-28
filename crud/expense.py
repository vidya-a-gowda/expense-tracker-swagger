from datetime import date
from typing import Any

from sqlalchemy.orm import Session

from models.expense import Expense
from schemas.expense import ExpenseCreate, ExpenseUpdate


class ExpenseCRUD:
    @staticmethod
    def create_expense(db: Session, expense_data: ExpenseCreate) -> Expense:
        db_expense = Expense(**expense_data.model_dump())
        db.add(db_expense)
        db.commit()
        db.refresh(db_expense)
        return db_expense

    @staticmethod
    def get_expenses(db: Session, category: str = None, start_date: date = None, end_date: date = None):
        query = db.query(Expense)

        if category:
            query = query.filter(Expense.category.ilike(category))
        if start_date:
            query = query.filter(Expense.date >= start_date)
        if end_date:
            query = query.filter(Expense.date <= end_date)

        return query.all()

    @staticmethod
    def get_expense_by_id(db: Session, expense_id: int) -> Expense | None:
        return db.query(Expense).filter(Expense.id == expense_id).first()

    @staticmethod
    def update_expense(db: Session, expense_id: int, expense_update: ExpenseUpdate) -> Expense | None:
        db_expense = ExpenseCRUD.get_expense_by_id(db, expense_id)
        if not db_expense:
            return None

        for key, value in expense_update.model_dump(exclude_unset=True).items():
            if value is not None:
                setattr(db_expense, key, value)

        db.commit()
        db.refresh(db_expense)
        return db_expense

    @staticmethod
    def delete_expense(db: Session, expense_id: int) -> bool:
        db_expense = ExpenseCRUD.get_expense_by_id(db, expense_id)
        if not db_expense:
            return False
        db.delete(db_expense)
        db.commit()
        return True

    @staticmethod
    def get_summary(db: Session) -> dict[str, Any]:
        expenses = db.query(Expense).all()

        if not expenses:
            return {"total_spent": 0.0, "category_breakdown": {}, "highest_expense": None}

        total_spent = sum(e.amount for e in expenses)
        breakdown: dict[str, float] = {}
        for e in expenses:
            breakdown[e.category] = breakdown.get(e.category, 0.0) + e.amount

        highest = max(expenses, key=lambda e: e.amount)
        highest_data = {
            "id": highest.id,
            "amount": highest.amount,
            "category": highest.category,
            "description": highest.description,
            "date": highest.date.isoformat(),
        }

        return {
            "total_spent": round(total_spent, 2),
            "category_breakdown": {k: round(v, 2) for k, v in breakdown.items()},
            "highest_expense": highest_data,
        }
