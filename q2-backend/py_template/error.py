from werkzeug.exceptions import HTTPException

class NonExistentNameError(HTTPException):
    code = 400

class NonExistentAnimalTypeError(HTTPException):
    code = 401