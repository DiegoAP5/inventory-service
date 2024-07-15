from typing import Any
from http import HTTPStatus
from flask import jsonify

class BaseResponse:
    def __init__(self, data: Any, message: str, success: bool, status: HTTPStatus):
        self.data = data
        self.message = message
        self.success = success
        self.status = status

    def to_dict(self):
        return {
            "data": self.data,
            "message": self.message,
            "success": self.success,
            "status": self.status.phrase
        }

    def to_response(self):
        response = jsonify(self.to_dict())
        response.status_code = self.status
        return response
