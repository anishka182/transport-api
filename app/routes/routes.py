from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models import Route
from app.schemas import RouteCreate, RouteResponse

router = APIRouter(prefix="/routes", tags=["Routes"])


@router.post("/", response_model=RouteResponse)
async def create_route(route: RouteCreate, db: AsyncSession = Depends(get_db)):
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


@router.get("/", response_model=list[RouteResponse])
async def get_all_routes(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Route))
    return result.scalars().all()


@router.get("/{route_id}", response_model=RouteResponse)
async def get_route(route_id: int, db: AsyncSession = Depends(get_db)):
    route = await db.get(Route, route_id)
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    return route


@router.put("/{route_id}", response_model=RouteResponse)
async def update_route(route_id: int, route: RouteCreate, db: AsyncSession = Depends(get_db)):
    db_route = await db.get(Route, route_id)
    if not db_route:
        raise HTTPException(status_code=404, detail="Route not found")

    db_route.route_number = route.route_number
    db_route.daily_passenger_count = route.daily_passenger_count
    db_route.fare = route.fare
    db_route.num_vehicles_on_route = route.num_vehicles_on_route

    await db.commit()
    await db.refresh(db_route)
    return db_route


@router.delete("/{route_id}")
async def delete_route(route_id: int, db: AsyncSession = Depends(get_db)):
    route = await db.get(Route, route_id)
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")

    await db.delete(route)
    await db.commit()
    return {"message": "Route deleted successfully"}
