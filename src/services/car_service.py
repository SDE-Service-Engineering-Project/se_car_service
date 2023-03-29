from datetime import datetime

from bson import ObjectId
from pymongo.collection import Collection

from src.dto.dtos import ModifyCarDTO, CreateCarDTO, CreateCarConfirmedDTO
from src.models.car import Car


class CarService:
    def __init__(self, db):
        self.db = db
        self.collection: Collection = self.db.get_collection(collection_name="cars")

    def fetch_all_cars(self):
        return [Car.fromMongo(x).toReadDTO() for x in list(self.collection.find())]

    def fetch_one_car(self, id: str):
        return Car.fromMongo(self.collection.find_one({"_id": ObjectId(id)})).toReadDTO()

    def fetch_available_cars(self):
        pass

    def insert_car(self, car_create_dto: CreateCarDTO):
        car = Car.fromCreateDTO(car_create_dto)
        new_car = self.collection.insert_one(car.dict())
        return CreateCarConfirmedDTO(id=str(new_car.inserted_id))

    def modify_car(self, id: str, car_modify_dto: ModifyCarDTO):
        modification_data = car_modify_dto.dict()
        modification_data["modifiedOn"] = datetime.now()
        self.collection.update_one({"_id": ObjectId(id)}, {"$set": modification_data})
        updated_car = self.collection.find_one({"_id": ObjectId(id)})
        return Car.fromMongo(updated_car).toReadDTO()

    def delete_car(self, id: str):
        self.collection.delete_one({"_id": ObjectId(id)})

    def delete_all_cars(self):
        self.collection.delete_many({})
