from datetime import datetime

from pydantic import BaseModel

from src.dto.dtos import CarReadDTO, CarCreateDTO


class Car(BaseModel):
    _id: str
    createdOn: datetime
    brand: str
    model: str
    construction_year: int
    price: float
    currency: str

    def toDTO(self):
        return CarReadDTO(id=self._id, createdOn=self.createdOn, brand=self.brand, model=self.model,
                          construction_year=self.construction_year, price=self.price, currency=self.currency)

    @staticmethod
    def fromDTO(dto: CarCreateDTO):
        return Car(createdOn=datetime.now(), brand=dto.brand, model=dto.model,
                   construction_year=dto.construction_year, price=dto.price, currency=dto.currency)
