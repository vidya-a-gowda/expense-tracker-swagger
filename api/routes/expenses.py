from datetime import date
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from crud.expense import ExpenseCRUD
from db.database import get_db
from schemas.expense import ExpenseCreate, ExpenseResponse, ExpenseSummary, ExpenseUpdate

router = APIRouter()


@router.post("/expenses/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED, tags=["Expenses"])
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    return ExpenseCRUD.create_expense(db=db, expense_data=expense)


@router.get("/expenses/summary", response_model=ExpenseSummary, tags=["Analytics"])
def get_expense_summary(db: Session = Depends(get_db)):
    return ExpenseCRUD.get_summary(db)


@router.get("/expenses/", response_model=List[ExpenseResponse], tags=["Expenses"])
def read_expenses(
    db: Session = Depends(get_db),
    category: str = Query(None, description="Filter expenses by category (case-insensitive)."),
    start_date: date = Query(None, description="Filter expenses from this date onwards (YYYY-MM-DD)."),
    end_date: date = Query(None, description="Filter expenses up to this date (YYYY-MM-DD)."),
):
    return ExpenseCRUD.get_expenses(db, category, start_date, end_date)


@router.get("/expenses/{expense_id}", response_model=ExpenseResponse, tags=["Expenses"])
def read_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = ExpenseCRUD.get_expense_by_id(db, expense_id)
    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense record not found.")
    return expense


@router.put("/expenses/{expense_id}", response_model=ExpenseResponse, tags=["Expenses"])
def update_expense(expense_id: int, expense_update: ExpenseUpdate, db: Session = Depends(get_db)):
    updated_expense = ExpenseCRUD.update_expense(db, expense_id, expense_update)
    if not updated_expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense record not found to update.")
    return updated_expense


@router.delete("/expenses/{expense_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Expenses"])
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    success = ExpenseCRUD.delete_expense(db, expense_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense record not found to delete.")
    return None
