from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models import Path
from app.schemas import PathCreate, PathResponse

router = APIRouter(prefix="/paths", tags=["Paths"])


@router.post("/", response_model=PathResponse)
async def create_path(path: PathCreate, db: AsyncSession = Depends(get_db)):
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


@router.get("/", response_model=list[PathResponse])
async def get_all_paths(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Path))
    return result.scalars().all()


@router.get("/{path_id}", response_model=PathResponse)
async def get_path(path_id: int, db: AsyncSession = Depends(get_db)):
    path = await db.get(Path, path_id)
    if not path:
        raise HTTPException(status_code=404, detail="Path not found")
    return path


@router.put("/{path_id}", response_model=PathResponse)
async def update_path(path_id: int, path: PathCreate, db: AsyncSession = Depends(get_db)):
    db_path = await db.get(Path, path_id)
    if not db_path:
        raise HTTPException(status_code=404, detail="Path not found")

    db_path.starting_point = path.starting_point
    db_path.end_point = path.end_point
    db_path.num_stops = path.num_stops
    db_path.distance = path.distance

    await db.commit()
    await db.refresh(db_path)
    return db_path


@router.delete("/{path_id}")
async def delete_path(path_id: int, db: AsyncSession = Depends(get_db)):
    path = await db.get(Path, path_id)
    if not path:
        raise HTTPException(status_code=404, detail="Path not found")

    await db.delete(path)
    await db.commit()
    return {"message": "Path deleted successfully"}
