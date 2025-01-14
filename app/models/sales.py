from pydantic import BaseModel
from sqlmodel import Field, SQLModel
from typing import Dict, List
from datetime import datetime


class IceCreamSaleSize(BaseModel):
   id: int
   name: str
   price: int

class SaleToppings(BaseModel):
   id: int
   name: str
   price_per_scoop: int
   scoops: int 

class SaleFlavor(BaseModel):
   flavor_name: str
   id: int

class CustomerProducts(BaseModel):
    count: int
    flavor: SaleFlavor
    type: str
    size: IceCreamSaleSize
    toppings: List[SaleToppings]
    basePrice: float
    totalPrice: float

class SalesBilling(BaseModel):
    customer_name: str
    purchases: List[CustomerProducts]
    payment_type: str
    total_amount: str
    amount_given: int | None
    amount_returned: str | None


class Customer(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(default=None, nullable=False)
    contact: str = Field(default=None, nullable=True)
    dob: datetime | None = Field(default=None, nullable=True)  # Changed to datetime
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)  # New column
    modified_at: datetime | None = Field(default=None, nullable=True)  # New column



class BillItemsToppings(SQLModel, table=True):
   id: int | None = Field(default=None, primary_key=True)
   bill_item_id: int = Field(nullable=False, description="Bill ITEM FK")
   topping_id: int = Field(nullable=False, description="Toppings id")
   no_of_scoops: int = Field(nullable=False, description="Number of scoops")
   topping_cost: int = Field(nullable=False, description="no_of_scoops * toppings price")
   created_at: datetime = Field(default_factory=datetime.now, nullable=False)  # New column
   modified_at: datetime | None = Field(default=None, nullable=True)  # New column



class BillItems(SQLModel, table=True):
   id: int | None = Field(default=None, primary_key=True)
   bill_id: int = Field(nullable=False)
   flavor_id: int = Field(nullable=False)
   flavor_type: str = Field(nullable=False)
   flavor_size: int = Field(nullable=False)
   base_price: float  = Field(nullable=False)
   total_price: float = Field(nullable=False, description="base price + toppings price")
   created_at: datetime = Field(default_factory=datetime.now, nullable=False)  # New column
   modified_at: datetime | None = Field(default=None, nullable=True)  # New column


class Bill(SQLModel, table=True):
   id: int | None = Field(default=None, primary_key=True)
   customer_id: int = Field(nullable=False)
   payment_type: str = Field(nullable=False)
   total_bill: int = Field(nullable=False)
   amount_given: int = Field(nullable=False)
   amount_returned: int | None = Field(nullable=True)
   created_at: datetime = Field(default_factory=datetime.now, nullable=False)  # New column
   modified_at: datetime | None = Field(default=None, nullable=True)  # New column

