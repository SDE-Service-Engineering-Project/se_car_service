from starlite import Controller, get, State, post, Body, delete, head, put

from src.dto.car_dto import ReadCarDTO, ModifyCarDTO, CreateCarDTO


class CarController(Controller):
    path = "/api/v1/cars"

    @get("/", description="List all cars.")
    async def list_cars(self, state: State) -> list[ReadCarDTO]:
        return state.car_service.fetch_all_cars()

    @get("/{id:str}", description="Get a car by id.")
    async def get_car(self, state: State, id: str) -> ReadCarDTO:
        return state.car_service.fetch_one_car(id=id)

    @get("/available", description="List all available cars.")
    async def list_available_cars(self, neededFrom: int, neededTo: int, state: State) -> list[ReadCarDTO]:
        return state.car_service.fetch_available_cars(neededFrom, neededTo)

    @head("/{id:str}", description="Check if a car exists.")
    async def ensure_car_existence(self, id: str, state: State) -> None:
        state.car_service.check_car_existence(id=id)

    @post("/", media_type="application/json", description="Create a car.")
    async def create_car(self, state: State, data: CreateCarDTO) -> ModifyCarDTO:
        return state.car_service.insert_car(car_create_dto=data)

    @put("/{id:str}", media_type="application/json", description="Update a car.")
    async def update_car(self, state: State, id: str, data: ModifyCarDTO = Body(title="Update car",
                                                                                description="Update an existing car.")) -> ReadCarDTO:
        return state.car_service.modify_car(id=id, car_modify_dto=data)

    @delete("/{id:str}", description="Delete a car.")
    async def delete_car(self, state: State, id: str) -> None:
        state.car_service.delete_car(id=id)

    @delete("/", description="Delete all cars.")
    async def delete_all_cars(self, state: State) -> None:
        state.car_service.delete_all_cars()
