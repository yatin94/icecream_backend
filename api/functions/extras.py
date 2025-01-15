from database import SessionDep
from models.extra import IceCreamSize
from models.flavors import FlavorSizes
from sqlmodel import select



async def create_size(flavor_size: FlavorSizes, flavor_id: int, session: SessionDep):
    if flavor_size.small:
        small_size = IceCreamSize(name='Small', price=flavor_size.small, flavor_id=flavor_id)
        session.add(small_size)
        session.commit()
        session.refresh(small_size)
    if flavor_size.medium:
        medium_size = IceCreamSize(name='Medium', price=flavor_size.medium, flavor_id=flavor_id)
        session.add(medium_size)
        session.commit()
        session.refresh(medium_size)
    if flavor_size.large:
        large_size = IceCreamSize(name='Large', price=flavor_size.large, flavor_id=flavor_id)
        session.add(large_size)
        session.commit()
        session.refresh(large_size)


async def activate_type_by_flavor(flavor_id: int, session: SessionDep, commit=True):
    pass
    # statement = select(IceCreamType).where(IceCreamType.flavor_id == flavor_id)
    # results = session.exec(statement=statement)
    # types = results.all()
    # for type in types:
    #     type.is_deleted = 0
    # session.add_all(types)
    # session.commit()
    # for type in types:
    #     session.refresh(type)
    # # session.refresh(types)

async def deactivate_type_by_flavor(flavor_id: int, session: SessionDep, commit=True):
    pass
    # statement = select(IceCreamType).where(IceCreamType.flavor_id == flavor_id)
    # results = session.exec(statement=statement)
    # types = results.all()
    # for type in types:
    #     type.is_deleted = 1
    # session.add_all(types)
    # session.commit()
    # for type in types:
    #     session.refresh(type)

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

def get_sizes(flavor_id: int, session: SessionDep):
    statement = select(IceCreamSize).where(IceCreamSize.flavor_id == flavor_id, IceCreamSize.is_deleted==0)
    results = session.exec(statement=statement)
    sizes = results.all()
    return sizes

# def get_type_by_id(type_id, session: SessionDep):
#     result: IceCreamType = session.get(IceCreamType, type_id)
#     # results = session.exec(statement=statment)
#     return result.dict()
