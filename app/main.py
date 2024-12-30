from fastapi import FastAPI
from app.routes import transport_types_router, routes_router, paths_router
from app.database import engine
from app.models import Base

app = FastAPI()

app.include_router(transport_types_router)
app.include_router(routes_router)
app.include_router(paths_router)



@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
