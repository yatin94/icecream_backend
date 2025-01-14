from fastapi import APIRouter
from models.flavors import Flavors, CreateFlavor, GetFlavorsResponse
from typing import List
from database import SessionDep
from sqlalchemy import delete
from sqlalchemy import text
from api.functions.extras import get_sizes
from api.functions.flavors import activate_flavor_by_id, deactivate_flavor_by_id, create_new_flavor

router = APIRouter()

@router.post("/flavors")
async def create_flavors(flavor: CreateFlavor, session: SessionDep):
    await create_new_flavor(flavor_data=flavor, session=session)
    return {"message":"success"}


@router.get("/flavors")
async def get_flavors(session: SessionDep, all: str = 'False', type: str = 'all'):
    print(all)
    if all == "True":
        raw_sql = f"""
            SELECT *
            FROM Flavors 
            WHERE is_deleted = 0
        """
    else:
        raw_sql = f"""
            SELECT *
            FROM Flavors 
            WHERE is_activated = 1 AND is_deleted = 0
        """
    if type == "cone":
        raw_sql += " AND is_sundae = 0"
    elif type == 'sundae':
        raw_sql += " AND is_sundae = 1"
    result = session.exec(text(raw_sql))
    flavor_dict = []
    for row in result:
        flavor_dict.append(GetFlavorsResponse(
            flavor_name=row[0],
            id=row[1],
            is_sundae=row[2],
            is_deleted=row[3],
            is_activated=row[4],
            size=get_sizes(row[1], session=session),
        ))
    return flavor_dict




@router.delete("/flavors/{id}")
async def delete_flavors(id: int, session: SessionDep):
    flavor = session.get(Flavors, id)
    flavor.is_deleted = 1
    flavor.is_activated = 0
    flavor = session.get(Flavors, id)
    update_size = text(f"update IceCreamSize set is_deleted = 1 where flavor_id = {flavor.id}")
    session.exec(update_size)
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




