from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from app.database import get_db
from app.models import Route, TransportType
from app.schemas import RouteCreate, RouteResponse
from app.models import Route, TransportType, Path


router = APIRouter(prefix="/routes", tags=["Routes"])



@router.get("/filter")
async def get_filtered_routes(
    min_passengers: int = Query(1000, alias="minPassengers"),
    max_fare: float = Query(50.0, alias="maxFare"),
    db: AsyncSession = Depends(get_db)
):
    try:
        result = await db.execute(
            select(Route).filter(
                Route.daily_passenger_count > min_passengers,
                Route.fare < max_fare
            )
        )
        return result.scalars().all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/with-transport")
async def get_routes_with_transport(db: AsyncSession = Depends(get_db)):
    try:
        results = await db.execute(
            select(Route, TransportType.name)
            .join(TransportType, TransportType.id == Route.transport_type_id)
        )
        return [
            {
                "route_id": route.id,
                "route_number": route.route_number,
                "daily_passenger_count": route.daily_passenger_count,
                "fare": route.fare,
                "num_vehicles_on_route": route.num_vehicles_on_route,
                "transport_name": transport_name
            }
            for route, transport_name in results
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/update-passengers")
async def update_passenger_count(distance_threshold: float = 100.0, db: AsyncSession = Depends(get_db)):
    try:
        
        subquery = (
            select(Path.route_id)
            .where(Path.distance > distance_threshold)
            .distinct()
        )

        
        stmt = (
            update(Route)
            .where(Route.id.in_(subquery))
            .values(daily_passenger_count=Route.daily_passenger_count + 100)
        )
        await db.execute(stmt)
        await db.commit()
        return {"message": "Routes updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sorted")
async def get_sorted_routes(
    sort_by: str = Query("fare", alias="sortBy"),
    descending: bool = Query(False, alias="desc"),
    db: AsyncSession = Depends(get_db)
):
    valid_sort_fields = ["fare", "route_number", "daily_passenger_count", "num_vehicles_on_route"]
    
    if sort_by not in valid_sort_fields:
        raise HTTPException(status_code=400, detail="Invalid sort field")
    
    
    order = Route.__table__.c[sort_by].desc() if descending else Route.__table__.c[sort_by]
    
    try:
        result = await db.execute(select(Route).order_by(order))
        routes = result.scalars().all()
        return routes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



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