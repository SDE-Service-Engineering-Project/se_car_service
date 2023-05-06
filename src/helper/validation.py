from bson import ObjectId
from bson.errors import InvalidId
from starlite import ValidationException


def validate_object_id(function):
    def wrapper(*args, **kwargs):
        object_id = kwargs.get("id")
        try:
            ObjectId(object_id)
        except InvalidId:
            message = f"The id {object_id} does not conform the the ObjectId format."
            raise ValidationException(detail=message)
        return function(*args, **kwargs)

    return wrapper
