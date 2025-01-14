from fastapi import APIRouter
from models.extra import IceCreamSize
from database import SessionDep
from sqlalchemy import text

router = APIRouter()

@router.post("/sizes")
async def create_size(size: IceCreamSize, session: SessionDep):
    session.add(size)
    session.commit()
    session.refresh(size)
    return {"message":"success"}

@router.get("/sizes")
async def get_size(session: SessionDep):
    raw_sql = text("SELECT * FROM IceCreamSize where is_deleted = 0")
    result = session.exec(raw_sql)
    sizes = [IceCreamSize(**row) for row in result.mappings().all()]
    return sizes

@router.get("/sizes/{flavor_id}")
async def get_specific_size(flavor_id: str, session: SessionDep):
    raw_sql = text(f"SELECT * FROM IceCreamSize where is_deleted = 0 and flavor_id = {flavor_id}")
    result = session.exec(raw_sql)
    sizes = [IceCreamSize(**row) for row in result.mappings().all()]
    return sizes

@router.delete("/sizes/{id}")
async def delete_size(id: int, session: SessionDep) -> dict:
    size = session.get(IceCreamSize, id)
    size.is_deleted = 1
    session.add(size)
    session.commit()
    session.refresh(size)
    return {"message":"success"}



