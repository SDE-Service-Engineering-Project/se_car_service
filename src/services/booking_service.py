import json
import logging

from bson import ObjectId
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError

from src.dto.booking_dto import KafkaBookingDTO

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
                self.insert_booking(kafka_booking)
            case "update":
                self.update_booking(kafka_booking)
            case "delete":
                self.delete_booking(kafka_booking.id)

    def insert_booking(self, booking_create_dto: KafkaBookingDTO) -> None:
        booking_dict = booking_create_dto.dict()
        booking_dict["_id"] = ObjectId(booking_dict.pop("id"))
        try:
            new_booking = self.collection.insert_one(booking_dict)  #
            log.info(f"Booking created: {new_booking.inserted_id}")
        except DuplicateKeyError as e:
            log.error(f"Could not insert booking: {e}")

    def update_booking(self, booking_modify_dto: KafkaBookingDTO) -> None:
        booking_dict = booking_modify_dto.dict()
        booking_dict["_id"] = ObjectId(booking_dict.pop("id"))
        self.collection.update_one({"_id": ObjectId(booking_dict['_id'])}, {"$set": booking_dict})
        log.info(f"Booking updated: {booking_modify_dto.id}")

    def delete_booking(self, id: str) -> None:
        self.collection.delete_one({"_id": ObjectId(id)})
        log.info(f"Booking updated: {id}")

    def _get_collection(self, collection_name):
        return self.db.get_collection(collection_name=collection_name)
