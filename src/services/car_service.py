from pymongo.collection import Collection

from src.dto.dtos import CarCreateDTO
from src.models.car import Car


class CarService:
    def __init__(self, db):
        self.db = db
        self.collection: Collection = self.db.get_collection(collection_name="cars")

    def fetch_all_cars(self):
        return [Car.toDTO(x) for x in list(self.collection.find())]

    def fetch_one_car(self, id: str):
        pass

    def fetch_available_cars(self):
        pass

    def insert_car(self, car: CarCreateDTO):
        car = Car.fromDTO(car)
        new_car = self.collection.insert_one(car)
        return new_car
