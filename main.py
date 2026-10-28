from fastapi import FastAPI

from api.routes.expenses import router as expenses_router
from db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ExpenseFlow API",
    description="A complete backend application to track, manage, and analyze personal expenses.",
    version="1.0.0",
)

app.include_router(expenses_router)
