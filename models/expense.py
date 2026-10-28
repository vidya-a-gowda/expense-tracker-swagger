from sqlalchemy import Column, Date, Float, Integer, String
from db.database import Base


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    category = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    date = Column(Date, nullable=False)
