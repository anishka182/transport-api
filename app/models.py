from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB


Base = declarative_base()

class TransportType(Base):
    __tablename__ = "transport_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    avg_speed = Column(Float, nullable=False)
    fleet_size = Column(Integer, nullable=False)
    fuel_consumption = Column(Float, nullable=False)
    is_electric = Column(Boolean, nullable=False, default=False)  
    specifications = Column(JSONB, nullable=True)

    routes = relationship("Route", back_populates="transport_type")


class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True)
    route_number = Column(Integer, nullable=False)
    daily_passenger_count = Column(Integer, nullable=False)
    fare = Column(Float, nullable=False)
    num_vehicles_on_route = Column(Integer, nullable=False)
    transport_type_id = Column(Integer, ForeignKey("transport_types.id"))

    transport_type = relationship("TransportType", back_populates="routes")
    paths = relationship("Path", back_populates="route")


class Path(Base):
    __tablename__ = "paths"

    id = Column(Integer, primary_key=True, index=True)
    starting_point = Column(String, nullable=False)
    end_point = Column(String, nullable=False)
    num_stops = Column(Integer, nullable=False)
    distance = Column(Float, nullable=False)
    route_id = Column(Integer, ForeignKey("routes.id"))

    route = relationship("Route", back_populates="paths")
