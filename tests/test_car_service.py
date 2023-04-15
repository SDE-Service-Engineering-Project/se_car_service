import json
import os
from unittest.mock import Mock, patch

from _pytest.fixtures import fixture
from pymongo.collection import Collection
from pymongo.database import Database

from src.dto.car_dto import CreateCarDTO, ModifyCarDTO
from src.services.car_service import CarService

# Get the directory containing the test file
test_file_dir = os.path.dirname(os.path.abspath(__file__))


@fixture(scope="module")
@patch("src.services.car_service.CarService._get_collection")
def car_service(mock_get):
    service = CarService(db=Mock(Database), car_collection_name="cars", booking_collection_name="bookings")
    mock_get.return_value = Mock(Collection)
    return service


@fixture(scope="module")
def mongo_car_list():
    file_path = os.path.join(test_file_dir, "resources/cars_mongo.json")
    with open(file_path) as f:
        return json.load(f)


@fixture(scope="module")
def dto_car_list():
    file_path = os.path.join(test_file_dir, "resources/cars_readDTO.json")
    with open(file_path) as f:
        return json.load(f)


def test_fetch_all_cars_assert_size(car_service, mongo_car_list):
    car_service.car_collection.find.return_value = mongo_car_list
    assert len(car_service.fetch_all_cars()) == 2


def test_fetch_all_cars_assert_fields(car_service, mongo_car_list):
    car_service.car_collection.find.return_value = mongo_car_list
    assert list(dict(car_service.fetch_all_cars()[0]).keys()) == ["carId", "brand", "model", "constructionYear", "price",
                                                                  "currency", "createdOn", "modifiedOn"]


def test_fetch_one_car(car_service, mongo_car_list, dto_car_list):
    car_service.car_collection.find_one.return_value = mongo_car_list[0]
    assert car_service.fetch_one_car(id="64254a66a468c0902635a358").json() == json.dumps(dto_car_list[0])


def test_insert_car_success(car_service):
    new_id = "64254a66a468c0902635a358"
    car_service.car_collection.insert_one.return_value = Mock(inserted_id=new_id)
    car_create_dto = CreateCarDTO(**{
        "brand": "Toyota",
        "model": "Cambri",
        "constructionYear": 1955,
        "price": 12000,
        "currency": "EUR"
    })
    response = car_service.insert_car(car_create_dto=car_create_dto)
    assert response.carId == new_id


def test_modify_car(car_service, mongo_car_list, dto_car_list):
    modify_car_dto = ModifyCarDTO(**{
        "brand": "Toyota",
        "model": "Cambri",
        "constructionYear": 1955,
        "price": 12000,
        "currency": "EUR"
    })
    car_service.car_collection.find_one.return_value = mongo_car_list[0]
    car_service.car_collection.update_one.return_value = Mock(matched_count=1)

    response = car_service.modify_car(id="64254a66a468c0902635a358", car_modify_dto=modify_car_dto)
    assert response.json() == json.dumps(dto_car_list[0])
