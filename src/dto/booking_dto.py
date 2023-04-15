from pydantic import BaseModel, Field


class KafkaBookingDTO(BaseModel):
    bookingId: str = Field(alias="_id")
    carId: str
    bookedFrom: int
    bookedUntil: int
    action: str

    class Config:
        allow_population_by_field_name = True


class KafkaBookingConfirmationDTO(BaseModel):
    id: str
