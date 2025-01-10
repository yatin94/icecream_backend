from typing import List
from sqlmodel import Field, SQLModel
from pydantic import BaseModel

class Flavors(SQLModel, table=True):
    flavor_name: str = Field(index=True)
    id: int | None = Field(default=None, primary_key=True)
    is_deleted: int = 0
    is_activated: int = 1




class FlavorSizes(SQLModel, table=False):
    small: int
    medium: int
    large: int

class FlavorTypes(SQLModel, table=False):
    sundae: FlavorSizes
    cone: FlavorSizes

class CreateFlavor(SQLModel, table=False):
    flavor_name: str = Field(index=True)
    types: FlavorTypes

