from pydantic import BaseModel
from typing import Optional


class TransportTypeCreate(BaseModel):
    name: str
    fleet_size: int
    fuel_consumption: float  
    avg_speed: float  


class TransportTypeResponse(TransportTypeCreate):
    id: int

    class Config:
        orm_mode = True


class RouteCreate(BaseModel):
    route_number: int
    daily_passenger_count: int
    fare: float
    num_vehicles_on_route: int


class RouteResponse(RouteCreate):
    id: int

    class Config:
        orm_mode = True


class PathCreate(BaseModel):
    starting_point: str  
    end_point: str
    num_stops: int  
    distance: float


class PathResponse(PathCreate):
    id: int

    class Config:
        orm_mode = True


class TransportTypeWithRoutesResponse(TransportTypeResponse):
    routes: list[RouteResponse] = []

    class Config:
        orm_mode = True
