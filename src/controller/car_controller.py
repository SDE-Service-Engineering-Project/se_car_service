from starlite import Controller, get, State, post

from src.auth.auth_controller import is_authorized
from src.dto.dtos import CarReadDTO


class CarController(Controller):
    path = "/cars"
    guards = [is_authorized]

    @get("/")
    async def list_cars(self, state: State) -> list[CarReadDTO]:
        return state.car_service.fetch_all_cars()

    @get("/{id:int}")
    async def get_car(self, state: State, id: str) -> CarReadDTO:
        return state.car_service.fetch_one_car(id=id)

    @get("/available")
    async def list_available_cars(self, state: State) -> list[CarReadDTO]:
        return state.car_service.fetch_available_cars()

    @post("/")
    async def create_car(self, state: State) -> dict:
        return state.car_service.insert_car(car=state.car)
