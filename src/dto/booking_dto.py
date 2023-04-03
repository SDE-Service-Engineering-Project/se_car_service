from pydantic import BaseModel, Field


class KafkaBookingDTO(BaseModel):
    id: str = Field(alias="_id")
    carId: str
    startDate: int
    endDate: int
    action: str

    class Config:
        allow_population_by_field_name = True


class KafkaBookingConfirmationDTO(BaseModel):
    id: str
