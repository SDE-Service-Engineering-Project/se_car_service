import json
import logging

from bson import ObjectId
from pymongo.collection import Collection

from src.dto.booking_dto import KafkaBookingDTO, KafkaBookingConfirmationDTO

log = logging.getLogger()


class BookingService:
    def __init__(self, db, collection_name):
        self.db = db
        self.collection: Collection = self._get_collection(collection_name)

    def handle_booking(self, message):
        kafka_booking = None
        try:
            message_dict = json.loads(message)
            kafka_booking = KafkaBookingDTO(**message_dict)
        except AttributeError as e:
            log.error(f"Could not parse message: {e}")
        match kafka_booking.action:
            case "create":
                result = self.insert_booking(kafka_booking)
                log.info(f"Booking created: {result.id}")
            case "update":
                result = self.update_booking(kafka_booking)
                log.info(f"Booking updated: {result.id}")
            case "delete":
                result = self.delete_booking(kafka_booking.id)
                log.info(f"Booking updated: {result.id}")

    def insert_booking(self, booking_create_dto: KafkaBookingDTO) -> KafkaBookingConfirmationDTO:
        booking_dict = booking_create_dto.dict()
        booking_dict["_id"] = ObjectId(booking_dict.pop("id"))
        new_booking = self.collection.insert_one(booking_dict)
        return KafkaBookingConfirmationDTO(id=str(new_booking.inserted_id))

    def update_booking(self, booking_modify_dto: KafkaBookingDTO) -> KafkaBookingConfirmationDTO:
        booking_dict = booking_modify_dto.dict()
        booking_dict["_id"] = ObjectId(booking_dict.pop("id"))
        self.collection.update_one({"_id": ObjectId(booking_dict['_id'])}, {"$set": booking_dict})
        return KafkaBookingConfirmationDTO(id=booking_modify_dto.id)

    def delete_booking(self, id: str) -> KafkaBookingConfirmationDTO:
        self.collection.delete_one({"_id": ObjectId(id)})
        return KafkaBookingConfirmationDTO(id=id)

    def _get_collection(self, collection_name):
        return self.db.get_collection(collection_name=collection_name)
