from datetime import datetime

from pydantic import BaseModel


class ReadCarDTO(BaseModel):
    carId: str
    brand: str
    model: str
    constructionYear: int
    price: float
    currency: str
    createdOn: datetime
    modifiedOn: datetime


class CreateCarDTO(BaseModel):
    brand: str
    model: str
    constructionYear: int
    price: float
    currency: str


class CreateCarConfirmedDTO(BaseModel):
    carId: str


class ModifyCarDTO(BaseModel):
    brand: str
    model: str
    constructionYear: int
    price: float
    currency: str
