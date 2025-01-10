from fastapi import APIRouter
from models.flavors import Flavors, CreateFlavor
from models.extra import IceCreamSize, IceCreamType
from typing import List
from database import SessionDep
from sqlalchemy import delete
from sqlalchemy import text

from api.functions.flavors import activate_flavor_by_id, deactivate_flavor_by_id, create_new_flavor

router = APIRouter()

@router.post("/flavors")
async def create_flavors(flavor: CreateFlavor, session: SessionDep):
    await create_new_flavor(flavor_data=flavor, session=session)
    return {"message":"success"}


@router.get("/flavors")
async def get_flavors(session: SessionDep, all: str = 'False'):
    if all == "True":
        raw_sql = text("SELECT * FROM Flavors where is_deleted=0")
    else:
        raw_sql = text("SELECT * FROM Flavors where is_activated = 1 and is_deleted=0")
    result = session.exec(raw_sql)
    flavors = [Flavors(**row) for row in result.mappings().all()]
    return flavors


@router.delete("/flavors/{id}")
async def delete_flavors(id: int, session: SessionDep):
    flavor = session.get(Flavors, id)
    flavor.is_deleted = 1
    flavor.is_activated = 0
    flavor = session.get(Flavors, id)
    update_type = text(f"update IceCreamType set is_deleted = 1 where flavor_id = {flavor.id}")
    update_size = text(f"update IceCreamSize set is_deleted = 1 where flavor_id = {flavor.id}")
    session.exec(update_size)
    session.exec(update_type)
    session.add(flavor)
    session.commit()
    return {"message":"success"}

from pydantic import BaseModel

class ChangeStatusBody(BaseModel):
    flavor_id: int
    status: str

@router.post("/flavors/change_status")
async def activate_flavor(data: ChangeStatusBody,  session: SessionDep):
    if data.status == 'activate':
        await activate_flavor_by_id(data.flavor_id, session=session)
    else:
        await deactivate_flavor_by_id(data.flavor_id, session=session)
    return {"message": "success"}




