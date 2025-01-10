# app/api/endpoints/topping.py
from fastapi import APIRouter, HTTPException
from typing import List
from models.toppings import Toppings
from database import SessionDep
from sqlalchemy import text


router = APIRouter()

@router.get("/toppings")
async def get_topping(session: SessionDep) -> List[Toppings]:
    raw_sql = text("SELECT * FROM Toppings where is_deleted = 0")
    result = session.exec(raw_sql)
    toppings = [Toppings(**row) for row in result.mappings().all()]
    return toppings

@router.post("/toppings")
async def create_topping(topping: Toppings, session: SessionDep):
    session.add(topping)
    session.commit()
    session.refresh(topping)
    return {"message":"success"}

@router.delete("/toppings/{id}")
async def delete_topping(id: int, session: SessionDep) -> dict:
    topping = session.get(Toppings, id)
    topping.is_deleted = 1
    session.add(topping)
    session.commit()
    session.refresh(topping)
    return {"message":"success"}