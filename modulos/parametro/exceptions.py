from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from agbc_servicio.response import ErrorRestResponse


class ServicioAuthenticationFailed(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = {
        'message': _('Incorrect authentication credentials..'),
        'type': 'error',
        'status': status_code
    }
    default_code = 'authentication_failed'

    def __init__(self, message):
        self.default_detail['message'] = message
        self.detail = self.default_detail