from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import TransportType, Route, Path
from app.schemas import TransportTypeCreate, RouteCreate, PathCreate



async def get_transport_types(db: AsyncSession):
    result = await db.execute(select(TransportType))
    return result.scalars().all()


async def get_transport_type_by_id(db: AsyncSession, transport_type_id: int):
    return await db.get(TransportType, transport_type_id)


async def create_transport_type(db: AsyncSession, transport_type: TransportTypeCreate):
    new_transport_type = TransportType(
        name=transport_type.name,
        avg_speed=transport_type.avg_speed,
        fleet_size=transport_type.fleet_size,
        fuel_consumption=transport_type.fuel_consumption,
        is_electric=transport_type.is_electric
    )
    db.add(new_transport_type)
    await db.commit()
    await db.refresh(new_transport_type)
    return new_transport_type


async def update_transport_type(
    db: AsyncSession, transport_type_id: int, transport_type: TransportTypeCreate
):
    db_transport_type = await db.get(TransportType, transport_type_id)
    if not db_transport_type:
        return None

    db_transport_type.name = transport_type.name
    db_transport_type.avg_speed = transport_type.avg_speed
    db_transport_type.fleet_size = transport_type.fleet_size
    db_transport_type.fuel_consumption = transport_type.fuel_consumption
    db_transport_type.is_electric=transport_type.is_electric

    await db.commit()
    await db.refresh(db_transport_type)
    return db_transport_type


async def delete_transport_type(db: AsyncSession, transport_type_id: int):
    transport_type = await db.get(TransportType, transport_type_id)
    if transport_type:
        await db.delete(transport_type)
        await db.commit()
        return True
    return False




async def get_routes(db: AsyncSession):
    result = await db.execute(select(Route))
    return result.scalars().all()


async def get_route_by_id(db: AsyncSession, route_id: int):
    return await db.get(Route, route_id)


async def create_route(db: AsyncSession, route: RouteCreate):
    new_route = Route(
        route_number=route.route_number,
        daily_passenger_count=route.daily_passenger_count,
        fare=route.fare,
        num_vehicles_on_route=route.num_vehicles_on_route,
    )
    db.add(new_route)
    await db.commit()
    await db.refresh(new_route)
    return new_route


async def update_route(db: AsyncSession, route_id: int, route: RouteCreate):
    db_route = await db.get(Route, route_id)
    if not db_route:
        return None

    db_route.route_number = route.route_number
    db_route.daily_passenger_count = route.daily_passenger_count
    db_route.fare = route.fare
    db_route.num_vehicles_on_route = route.num_vehicles_on_route

    await db.commit()
    await db.refresh(db_route)
    return db_route


async def delete_route(db: AsyncSession, route_id: int):
    route = await db.get(Route, route_id)
    if route:
        await db.delete(route)
        await db.commit()
        return True
    return False




async def get_paths(db: AsyncSession):
    result = await db.execute(select(Path))
    return result.scalars().all()


async def get_path_by_id(db: AsyncSession, path_id: int):
    return await db.get(Path, path_id)


async def create_path(db: AsyncSession, path: PathCreate):
    new_path = Path(
        starting_point=path.starting_point,
        end_point=path.end_point,
        num_stops=path.num_stops,
        distance=path.distance,
    )
    db.add(new_path)
    await db.commit()
    await db.refresh(new_path)
    return new_path


async def update_path(db: AsyncSession, path_id: int, path: PathCreate):
    db_path = await db.get(Path, path_id)
    if not db_path:
        return None

    db_path.starting_point = path.starting_point
    db_path.end_point = path.end_point
    db_path.num_stops = path.num_stops
    db_path.distance = path.distance

    await db.commit()
    await db.refresh(db_path)
    return db_path


async def delete_path(db: AsyncSession, path_id: int):
    path = await db.get(Path, path_id)
    if path:
        await db.delete(path)
        await db.commit()
        return True
    return False
