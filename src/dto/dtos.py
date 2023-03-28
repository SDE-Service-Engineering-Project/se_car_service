from dataclasses import dataclass
from datetime import datetime

from pydantic import BaseModel


@dataclass
class CarReadDTO(BaseModel):
    id: str
    createdOn: datetime
    brand: str
    model: str
    construction_year: int
    price: float
    currency: str


@dataclass
class CarCreateDTO(BaseModel):
    brand: str
    model: str
    construction_year: int
    price: float
    currency: str
