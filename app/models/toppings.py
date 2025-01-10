# app/models/topping.py
from typing import List
from sqlmodel import Field, SQLModel


class Toppings(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    price_per_scoop: int = Field(default=None, )
    is_deleted: int = 0

