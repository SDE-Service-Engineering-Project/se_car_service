from datetime import datetime

from bson import ObjectId
from pymongo.collection import Collection
from starlite import NotFoundException

from src.dto.car_dto import ModifyCarDTO, CreateCarDTO, CreateCarConfirmedDTO, ReadCarDTO
from src.helper.validation import validate_object_id
from src.models.car import Car


class CarService:
    def __init__(self, db, car_collection_name, booking_collection_name):
        self.db = db
        self.car_collection: Collection = self._get_collection(car_collection_name)
        self.booking_collection: Collection = self._get_collection(booking_collection_name)

    def fetch_all_cars(self) -> list[ReadCarDTO]:
        return [Car.fromMongo(x).toReadDTO() for x in list(self.car_collection.find())]

    @validate_object_id
    def fetch_one_car(self, id: str) -> ReadCarDTO:
        return_value: dict = self.car_collection.find_one({"_id": ObjectId(id)})
        if return_value is not None:
            return Car.fromMongo(return_value).toReadDTO()
        else:
            raise NotFoundException(f"Car with id {id} does not exist.")

    def fetch_available_cars(self, start_date: int, end_date: int) -> list[ReadCarDTO]:
        cars: list[ReadCarDTO] = self.fetch_all_cars()
        booked_car_ids: list[str] = [x["carId"] for x in self.booking_collection.find(
            {"$or": [{"startDate": {"$gte": start_date, "$lte": end_date}},
                     {"endDate": {"$gte": start_date, "$lte": end_date}}]})]
        return [x for x in cars if x.id not in booked_car_ids]

    @validate_object_id
    def check_car_existence(self, id: str) -> None:
        if self.car_collection.find_one({"_id": id}) is None:
            raise NotFoundException(f"Car with id {id} does not exist.")

    def insert_car(self, car_create_dto: CreateCarDTO) -> CreateCarConfirmedDTO:
        car = Car.fromCreateDTO(car_create_dto)
        new_car = self.car_collection.insert_one(car.dict())
        return CreateCarConfirmedDTO(id=str(new_car.inserted_id))

    @validate_object_id
    def modify_car(self, id: str, car_modify_dto: ModifyCarDTO) -> ReadCarDTO:
        modification_data = car_modify_dto.dict()
        modification_data["modifiedOn"] = datetime.now()
        update = self.car_collection.update_one({"_id": ObjectId(id)}, {"$set": modification_data})
        if update.matched_count == 0:
            raise NotFoundException(f"Car with id {id} does not exist.")
        updated_car = self.car_collection.find_one({"_id": ObjectId(id)})
        return Car.fromMongo(updated_car).toReadDTO()

    @validate_object_id
    def delete_car(self, id: str) -> None:
        return_value = self.car_collection.delete_one({"_id": ObjectId(id)})
        if return_value.deleted_count == 0:
            raise NotFoundException(f"Car with id {id} does not exist.")

    def delete_all_cars(self) -> None:
        self.car_collection.delete_many({})

    def _get_collection(self, collection_name):
        return self.db.get_collection(collection_name=collection_name)
