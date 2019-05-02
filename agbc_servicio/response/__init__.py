from rest_framework.response import Response

class SuccessRestResponse(Response):
    def __init__(self, message: str, status=200, data=None):
        super().__init__({
            'type': 'success',
            'message': message,
            'status': status,
            'data': data
        }, status=status)


class ErrorRestResponse(Response):
    def __init__(self, message: str, status=500, data=None):
        super().__init__({
            'type': 'error',
            'message': message,
            'status': status,
            'data': data
        }, status=status)


class WarningRestResponse(Response):
    def __init__(self, message: str, status=201, data=None):
        super().__init__({
            'type': 'warning',
            'message': message,
            'status': status,
            'data': data
        }, status=status)