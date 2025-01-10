# app/api/endpoints/topping.py
from fastapi import APIRouter, HTTPException
from typing import List
from models.purchases import Purchases
from database import SessionDep
from sqlalchemy import text


router = APIRouter()

@router.get("/purchases")
async def get_topping(session: SessionDep) -> List[Purchases]:
    raw_sql = text("SELECT * FROM Purchases where is_deleted = 0")
    result = session.exec(raw_sql)
    purchases = [Purchases(**row) for row in result.mappings().all()]
    return purchases

@router.post("/purchases")
async def create_topping(purchases: Purchases, session: SessionDep):
    session.add(purchases)
    session.commit()
    session.refresh(purchases)
    return {"message":"success"}

@router.delete("/purchases/{id}")
async def delete_topping(id: int, session: SessionDep) -> dict:
    purchase = session.get(Purchases, id)
    purchase.is_deleted = 1
    session.add(purchase)
    session.commit()
    session.refresh(purchase)
    return {"message":"success"}