from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from src.dto.car_dto import ReadCarDTO, CreateCarDTO


class Car(BaseModel):
    id: Optional[str]
    brand: str
    model: str
    construction_year: int
    price: float
    currency: str
    created_on: datetime
    modified_on: datetime

    def toReadDTO(self):
        return ReadCarDTO(
            carId=self.id,
            brand=self.brand,
            model=self.model,
            constructionYear=self.construction_year,
            price=self.price,
            currency=self.currency,
            createdOn=self.created_on,
            modifiedOn=self.modified_on
        )

    @staticmethod
    def fromCreateDTO(dto: CreateCarDTO):
        return Car(created_on=datetime.now(), modified_on=datetime.now(), brand=dto.brand, model=dto.model,
                   construction_year=dto.constructionYear, price=dto.price, currency=dto.currency)

    @staticmethod
    def fromMongo(dict_: dict):
        dict_['id'] = str(dict_["_id"])
        return Car(
            id=str(dict_['_id']),
            brand=dict_['brand'],
            model=dict_['model'],
            construction_year=dict_['construction_year'],
            price=dict_['price'],
            currency=dict_['currency'],
            created_on=dict_['created_on'],
            modified_on=dict_['modified_on']
        )
