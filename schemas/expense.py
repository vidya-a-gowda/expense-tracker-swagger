import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class ExpenseBase(BaseModel):
    amount: float = Field(..., gt=0, description="The amount of the expense. Must be greater than 0.")
    category: str = Field(..., min_length=1, max_length=50, description="The category of the expense. Cannot be empty.")
    description: Optional[str] = Field(None, max_length=200, description="Optional details about the expense.")
    date: datetime.date = Field(..., description="The date when the expense occurred (YYYY-MM-DD).")


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0, description="Updated expense amount.")
    category: Optional[str] = Field(None, min_length=1, max_length=50, description="Updated expense category.")
    description: Optional[str] = Field(None, max_length=200, description="Updated description.")
    date: Optional[datetime.date] = Field(None, description="Updated expense date.")


class ExpenseResponse(ExpenseBase):
    id: int

    class Config:
        from_attributes = True


class ExpenseSummary(BaseModel):
    total_spent: float
    category_breakdown: Dict[str, float]
    highest_expense: Dict[str, Any] | None
