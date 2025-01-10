from fastapi import APIRouter
from models.extra import IceCreamSize, IceCreamType
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

@router.get("/sizes/{flavor_id}/{type_id}")
async def get_specific_size(flavor_id: str, type_id: str, session: SessionDep):
    raw_sql = text(f"SELECT * FROM IceCreamSize where is_deleted = 0 and flavor_id = {flavor_id} and ice_cream_type_id = {type_id}")
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




@router.post("/types")
async def create_type(type: IceCreamType, session: SessionDep):
    session.add(type)
    session.commit()
    session.refresh(type)
    return {"message":"success"}


@router.get("/types/{flavor_id}")
async def get_type(flavor_id: int, session: SessionDep):
    raw_sql = text(f"SELECT * FROM IceCreamType where is_deleted = 0 and flavor_id = {flavor_id}")
    result = session.exec(raw_sql)
    types = [IceCreamType(**row) for row in result.mappings().all()]
    return types


@router.get("/types")
async def get_all_type(session: SessionDep):
    raw_sql = text("SELECT * FROM IceCreamType where is_deleted = 0")
    result = session.exec(raw_sql)
    types = [IceCreamType(**row) for row in result.mappings().all()]
    return types


@router.delete("/types/{id}")
async def delete_type(id: int, session: SessionDep):
    type = session.get(IceCreamType, id)
    type.is_deleted = 1
    session.add(type)
    session.commit()
    session.refresh(type)
    return {"message":"success"}
