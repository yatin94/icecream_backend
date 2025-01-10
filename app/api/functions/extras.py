from database import SessionDep
from models.extra import IceCreamType, IceCreamSize
from models.flavors import FlavorTypes, FlavorSizes
from sqlmodel import select


async def create_type(flavor_id: int, flavor_type: FlavorTypes, session: SessionDep):
    if flavor_type.sundae.small or flavor_type.sundae.medium or flavor_type.sundae.large:
        
        sundae_cream_obj = IceCreamType(type="Sundae", flavor_id=flavor_id)
        session.add(sundae_cream_obj)
        session.commit()
        session.refresh(sundae_cream_obj)
        await create_size(flavor_size=flavor_type.sundae, flavor_id=flavor_id, type_id=sundae_cream_obj.id, session=session)
    if flavor_type.cone.small and flavor_type.cone.medium and flavor_type.cone.large:
        cone_cream_obj = IceCreamType(type="Cone", flavor_id=flavor_id)
        session.add(cone_cream_obj)
        session.commit()
        session.refresh(cone_cream_obj)
        await create_size(flavor_size=flavor_type.cone, flavor_id=flavor_id, type_id=cone_cream_obj.id, session=session)
        
async def create_size(flavor_size: FlavorSizes, flavor_id: int, type_id: int, session: SessionDep):
    if flavor_size.small:
        small_size = IceCreamSize(name='Small', price=flavor_size.small, ice_cream_type_id=type_id, flavor_id=flavor_id)
        session.add(small_size)
        session.commit()
        session.refresh(small_size)
    if flavor_size.medium:
        medium_size = IceCreamSize(name='Medium', price=flavor_size.medium, ice_cream_type_id=type_id, flavor_id=flavor_id)
        session.add(medium_size)
        session.commit()
        session.refresh(medium_size)
    if flavor_size.large:
        large_size = IceCreamSize(name='Large', price=flavor_size.large, ice_cream_type_id=type_id, flavor_id=flavor_id)
        session.add(large_size)
        session.commit()
        session.refresh(large_size)


async def activate_type_by_flavor(flavor_id: int, session: SessionDep, commit=True):
    statement = select(IceCreamType).where(IceCreamType.flavor_id == flavor_id)
    results = session.exec(statement=statement)
    types = results.all()
    for type in types:
        type.is_deleted = 0
    session.add_all(types)
    session.commit()
    for type in types:
        session.refresh(type)
    # session.refresh(types)

async def deactivate_type_by_flavor(flavor_id: int, session: SessionDep, commit=True):
    statement = select(IceCreamType).where(IceCreamType.flavor_id == flavor_id)
    results = session.exec(statement=statement)
    types = results.all()
    for type in types:
        type.is_deleted = 1
    session.add_all(types)
    session.commit()
    for type in types:
        session.refresh(type)

async def activate_size_by_flavor(flavor_id: int, session: SessionDep, commit=True):
    statement = select(IceCreamSize).where(IceCreamSize.flavor_id == flavor_id)
    results = session.exec(statement=statement)
    sizes = results.all()
    for size in sizes:
        size.is_deleted = 0
    session.add_all(sizes)
    session.commit()
    for size in sizes:
        session.refresh(size)
    
    
async def deactivate_size_by_flavor(flavor_id: int, session: SessionDep, commit=True):
    statement = select(IceCreamSize).where(IceCreamSize.flavor_id == flavor_id)
    results = session.exec(statement=statement)
    sizes = results.all()
    for size in sizes:
        size.is_deleted = 1
    session.add_all(sizes)
    session.commit()
    for size in sizes:
        session.refresh(size)