from sqlmodel import select
from database import SessionDep
from models.flavors import Flavors, CreateFlavor
from api.functions.extras import create_size
import asyncio


async def create_new_flavor(flavor_data: CreateFlavor, session: SessionDep):
    is_sundae = 1 if flavor_data.sundae else 0
    flavor_obj = Flavors(flavor_name=flavor_data.flavor_name, is_deleted=0, is_sundae=is_sundae)
    session.add(flavor_obj)
    session.commit()
    session.refresh(flavor_obj)
    await create_size(flavor_data.sizes, flavor_obj.id, session)
    # await create_type(flavor_id=flavor_obj.id, flavor_type=flavor_data.types, session=session)



async def activate_flavor_by_id(flavor_id: int, session: SessionDep):
    statement = select(Flavors).where(Flavors.id == flavor_id)
    results = session.exec(statement=statement)
    flavor = results.one()
    flavor.is_activated = 1
    session.add(flavor)
    session.commit()
    session.refresh(flavor)



async def deactivate_flavor_by_id(flavor_id: int, session: SessionDep):
    statement = select(Flavors).where(Flavors.id == flavor_id)
    results = session.exec(statement=statement)
    flavor = results.one()
    flavor.is_activated = 0
    session.add(flavor)
    session.commit()
    session.refresh(flavor)