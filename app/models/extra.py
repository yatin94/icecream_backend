from pydantic import BaseModel
from typing import List
from sqlmodel import Field, SQLModel



class IceCreamSize(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    price: int = Field(default=None)
    flavor_id: int = Field(description="Flavor id")
    is_deleted: int = 0



# class IceCreamType(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     type: str = Field(index=True)
#     flavor_id: int = Field()
#     is_deleted: int = 0


