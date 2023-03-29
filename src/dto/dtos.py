from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ReadCarDTO(BaseModel):
    id: str
    brand: str
    model: str
    construction_year: int
    price: float
    currency: str
    createdOn: datetime
    modifiedOn: datetime


class CreateCarDTO(BaseModel):
    brand: str
    model: str
    construction_year: int
    price: float
    currency: str


class CreateCarConfirmedDTO(BaseModel):
    id: str


class ModifyCarDTO(BaseModel):
    brand: str
    model: str
    construction_year: int
    price: float
    currency: str
