from fastapi import APIRouter
from typing import Dict, List
from models.sales import SalesBilling, Bill, BillItems, BillItemsToppings, Customer, CustomerProducts, SaleToppings
from database import SessionDep
from sqlmodel import select

router = APIRouter()


@router.get("/sales/generate_bill_id")
async def create_size():
    return {"id": 22}


@router.post("/sales/")
async def create_billing(data: SalesBilling, session: SessionDep):
    to_refresh = []
    # Customer
    customer = select(Customer).where(Customer.name == data.customer_name)
    results = session.exec(statement=customer)
    customer_obj = results.one_or_none()
    if not customer_obj:
        customer_obj = Customer(name=data.customer_name, contact="dummy")
        session.add(customer_obj)
        session.flush()
        to_refresh.append(customer_obj)
    # Create Bill
    bill_obj = Bill(
        customer_id=customer_obj.id,
        payment_type=data.payment_type,
        total_bill=data.total_amount,
        amount_given=data.amount_given,
        amount_returned=data.amount_returned,
    )
    session.add(bill_obj)
    to_refresh.append(bill_obj)
    session.flush()


    # Process items
    items: List[CustomerProducts] = data.purchases
    for item in items:
        bill_item = BillItems(
            bill_id=bill_obj.id,
            flavor_id=item.flavor.id,
            flavor_size=item.size.id,
            flavor_type=item.type,
            base_price=item.basePrice,
            total_price=item.totalPrice
        )
        session.add(bill_item)
        session.flush()
        to_refresh.append(bill_item)

        # process toppings
        if item.toppings:
            toppings: List[SaleToppings] = item.toppings
            for topping in toppings:
                bill_item_toppings = BillItemsToppings(
                    bill_item_id=bill_item.id,
                    topping_id=topping.id,
                    no_of_scoops=topping.scoops,
                    topping_cost=topping.price_per_scoop * topping.scoops
                )
                session.add(bill_item_toppings)
                session.flush()
                to_refresh.append(bill_item_toppings)

    session.commit()
    for refresh_session in to_refresh:
        session.refresh(refresh_session)

    return {"next_id": 24}
