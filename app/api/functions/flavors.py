from sqlmodel import select
from database import SessionDep
from models.flavors import Flavors, CreateFlavor
from api.functions.extras import create_type, activate_type_by_flavor, activate_size_by_flavor, deactivate_size_by_flavor, deactivate_type_by_flavor
import asyncio


async def create_new_flavor(flavor_data: CreateFlavor, session: SessionDep):
    flavor_obj = Flavors(flavor_name=flavor_data.flavor_name, is_deleted=0)
    session.add(flavor_obj)
    session.commit()
    session.refresh(flavor_obj)
    await create_type(flavor_id=flavor_obj.id, flavor_type=flavor_data.types, session=session)



async def activate_flavor_by_id(flavor_id: int, session: SessionDep):
    statement = select(Flavors).where(Flavors.id == flavor_id)
    results = session.exec(statement=statement)
    flavor = results.one()
    # task1 = asyncio.create_task(activate_type_by_flavor(flavor_id=flavor.id, session=session,commit=False))
    # task2 = asyncio.create_task(activate_size_by_flavor(flavor_id=flavor.id, session=session, commit=False))
    flavor.is_activated = 1
    # results = await asyncio.gather(task1, task2)
    session.add(flavor)
    session.commit()
    session.refresh(flavor)



async def deactivate_flavor_by_id(flavor_id: int, session: SessionDep):
    statement = select(Flavors).where(Flavors.id == flavor_id)
    results = session.exec(statement=statement)
    flavor = results.one()
    # task1 = asyncio.create_task(deactivate_type_by_flavor(flavor_id=flavor.id, session=session,commit=False))
    # task2 = asyncio.create_task(deactivate_size_by_flavor(flavor_id=flavor.id, session=session, commit=False))
    flavor.is_activated = 0
    # results = await asyncio.gather(task1, task2)
    session.add(flavor)
    session.commit()
    session.refresh(flavor)