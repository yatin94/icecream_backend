# app/models/topping.py
from typing import List
from sqlmodel import Field, SQLModel
from datetime import datetime



class Purchases(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    price_per_unit: int = Field(default=None, )
    quantity: int = Field(default=None, )
    total_cost: int = Field(default=None, )
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)  # New column
    modified_at: datetime | None = Field(default=None, nullable=True)  # New column
    is_deleted: int = 0

