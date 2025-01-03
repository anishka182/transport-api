from fastapi import FastAPI, Depends, Query
from app.routes import transport_types_router, routes_router, paths_router
from app.database import engine, get_db
from app.models import Base
from app import crud
from fastapi.templating import Jinja2Templates
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()

app.include_router(transport_types_router)
app.include_router(routes_router)
app.include_router(paths_router)

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def index(request: Request, db: AsyncSession = Depends(get_db)):  
    transport_types = await crud.get_transport_types(db=db, skip=0, limit=5)
    routes = await crud.get_routes(db=db, skip=0, limit=5)
    paths = await crud.get_paths(db=db, skip=0, limit=5)
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "transport_types": transport_types["items"],
        "routes": routes["items"],
        "paths": paths["items"],
        "page_url": "index"
    })

@app.get("/transport-types/")
async def transport_types_page(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    db: AsyncSession = Depends(get_db)  
):
    transport_types = await crud.get_transport_types(db=db, skip=skip, limit=limit)
    current_page = (skip // limit) + 1
    total_pages = (transport_types["total"] + limit - 1) // limit
    return templates.TemplateResponse("transport_types_list.html", {
        "request": request,
        "transport_types": transport_types["items"],
        "skip": skip,
        "limit": limit,
        "total": transport_types["total"],
        "current_page": current_page,
        "total_pages": total_pages,
        "page_url": "transport-types"
    })

@app.get("/routes/")
async def routes_page(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    db: AsyncSession = Depends(get_db)  
):
    routes = await crud.get_routes(db=db, skip=skip, limit=limit)
    current_page = (skip // limit) + 1
    total_pages = (routes["total"] + limit - 1) // limit
    return templates.TemplateResponse("routes_list.html", {
        "request": request,
        "routes": routes["items"],
        "skip": skip,
        "limit": limit,
        "total": routes["total"],
        "current_page": current_page,
        "total_pages": total_pages,
        "page_url": "routes"
    })

@app.get("/paths/")
async def paths_page(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    db: AsyncSession = Depends(get_db)  
):
    paths = await crud.get_paths(db=db, skip=skip, limit=limit)
    current_page = (skip // limit) + 1
    total_pages = (paths["total"] + limit - 1) // limit
    return templates.TemplateResponse("paths_list.html", {
        "request": request,
        "paths": paths["items"],
        "skip": skip,
        "limit": limit,
        "total": paths["total"],
        "current_page": current_page,
        "total_pages": total_pages,
        "page_url": "paths"
    })

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
