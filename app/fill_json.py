import asyncio
from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select  
import json


DATABASE_URL = "postgresql+asyncpg://Ani22:1111@localhost:5432/transport_db"  # Убедитесь, что заменили на правильные данные

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


class TransportType(Base):
    __tablename__ = 'transport_types'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    specifications = Column(JSON)


async def fill_specifications():
    async with SessionLocal() as session:
        
        transport_types = await session.execute(select(TransportType))
        transport_types = transport_types.scalars().all()
        
        for transport in transport_types:
            
            specifications_data = {"key1": f"value_{transport.name}_1", "key2": f"value_{transport.name}_2"}
            transport.specifications = specifications_data
            
            
            session.add(transport)
        
        await session.commit()


asyncio.run(fill_specifications())
