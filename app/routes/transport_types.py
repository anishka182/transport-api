from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from app.database import get_db
from app.models import TransportType
from app.schemas import TransportTypeCreate, TransportTypeResponse

router = APIRouter(prefix="/transport-types", tags=["Transport Types"])

@router.post("/", response_model=TransportTypeResponse)
async def create_transport_type(
    transport_type: TransportTypeCreate, db: AsyncSession = Depends(get_db)
):
    new_transport_type = TransportType(
        name=transport_type.name,
        avg_speed=transport_type.avg_speed,
        fleet_size=transport_type.fleet_size,
        fuel_consumption=transport_type.fuel_consumption,
    )
    db.add(new_transport_type)
    await db.commit()
    await db.refresh(new_transport_type)
    return new_transport_type

@router.get("/", response_model=list[TransportTypeResponse])
async def get_all_transport_types(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TransportType))
    return result.scalars().all()

@router.get("/{transport_type_id}", response_model=TransportTypeResponse)
async def get_transport_type(
    transport_type_id: int, db: AsyncSession = Depends(get_db)
):
    transport_type = await db.get(TransportType, transport_type_id)
    if not transport_type:
        raise HTTPException(status_code=404, detail="Transport type not found")
    return transport_type

@router.put("/{transport_type_id}", response_model=TransportTypeResponse)
async def update_transport_type(
    transport_type_id: int,
    transport_type: TransportTypeCreate,
    db: AsyncSession = Depends(get_db),
):
    db_transport_type = await db.get(TransportType, transport_type_id)
    if not db_transport_type:
        raise HTTPException(status_code=404, detail="Transport type not found")

    db_transport_type.name = transport_type.name
    db_transport_type.avg_speed = transport_type.avg_speed
    db_transport_type.fleet_size = transport_type.fleet_size
    db_transport_type.fuel_consumption = transport_type.fuel_consumption

    await db.commit()
    await db.refresh(db_transport_type)
    return db_transport_type

@router.delete("/{transport_type_id}")
async def delete_transport_type(transport_type_id: int, db: AsyncSession = Depends(get_db)):
    transport_type = await db.get(TransportType, transport_type_id)
    if not transport_type:
        raise HTTPException(status_code=404, detail="Transport type not found")

    await db.delete(transport_type)
    await db.commit()
    return {"message": "Transport type deleted successfully"}

@router.get("/grouped-by-type", response_model=list)
async def group_by_transport(db: AsyncSession = Depends(get_db)):
    try:
        results = await db.execute(
            select(
                TransportType.name, func.sum(TransportType.fleet_size).label("total_fleet")
            ).group_by(TransportType.name)
        )
        
        return [{"transport_name": row[0], "total_fleet": row[1]} for row in results]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
