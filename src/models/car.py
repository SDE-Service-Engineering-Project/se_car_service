from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from src.dto.dtos import ReadCarDTO, CreateCarDTO


class Car(BaseModel):
    id: Optional[str]
    brand: str
    model: str
    construction_year: int
    price: float
    currency: str
    createdOn: datetime
    modifiedOn: datetime

    def toReadDTO(self):
        return ReadCarDTO(**self.__dict__)
        # return ReadCarDTO(id=self.id, createdOn=self.createdOn, brand=self.brand, model=self.model,
        #                   construction_year=self.construction_year, price=self.price, currency=self.currency)

    @staticmethod
    def fromCreateDTO(dto: CreateCarDTO):
        return Car(createdOn=datetime.now(), modifiedOn=datetime.now(), brand=dto.brand, model=dto.model,
                   construction_year=dto.construction_year, price=dto.price, currency=dto.currency)

    @staticmethod
    def fromMongo(dict_: dict):
        dict_['id'] = str(dict_["_id"])
        return Car(**dict_)
