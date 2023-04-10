from bson import ObjectId
from bson.errors import InvalidId
from starlite import ValidationException


def validate_object_id(function):
    def wrapper(*args, **kwargs):
        object_id = kwargs.get("id")
        try:
            ObjectId(object_id)
        except InvalidId:
            raise ValidationException(f"Invalid id {object_id}")
        return function(*args, **kwargs)
    return wrapper
