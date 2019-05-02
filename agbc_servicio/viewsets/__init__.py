from django.utils.translation import ugettext_lazy as _
from django.http import Http404
from django.core.exceptions import ValidationError as ModelValidationError
from django.db import DatabaseError
from rest_framework import status
from rest_framework.viewsets import ModelViewSet as OriginalModelViewSet
from rest_framework.viewsets import ViewSet as OriginalViewSet
from rest_framework.validators import ValidationError as RESTValidationError

from agbc_servicio.response import ErrorRestResponse, SuccessRestResponse
from agbc_servicio.excepciones import PermissionDenied, UserDoesnotAuthenticated, NotFound

class PermissionViewSetMixin:
    def permission_denied(self, request, message=None):
        """Overwrite permission exceptions"""
        if request.authenticators and not request.successful_authenticator:
            raise UserDoesnotAuthenticated()
        raise PermissionDenied()


class ViewSet(PermissionViewSetMixin, OriginalViewSet):
    pass


class ModelViewSet(PermissionViewSetMixin, OriginalModelViewSet):
    def create(self, request, *args, **kwargs):
        """Overrite response when a model is created"""
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
        except ModelValidationError as ex:
            return ErrorRestResponse(
                message=ex.message,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except RESTValidationError as ex:
            return ErrorRestResponse(
                message=_('There are problems with the data'),
                data=ex.detail,
                status=status.HTTP_400_BAD_REQUEST
            )
        except DatabaseError as ex:
            return ErrorRestResponse(str(ex))
        return SuccessRestResponse(
            message=_('Operation finish successly'),
            status=status.HTTP_201_CREATED,
            data=serializer.data
        )

    def update(self, request, *args, **kwargs):
        """Overwrite response when a object is created"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
        except ModelValidationError as ex:
            return ErrorRestResponse(
                message=ex.messages[0],
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except RESTValidationError as ex:
            return ErrorRestResponse(
                message=_('There are problems with the data'),
                status=status.HTTP_400_BAD_REQUEST,
                data=ex.detail
            )
        except DatabaseError as ex:
            return ErrorRestResponse(str(ex))

        if getattr(instance, '_prefetched_objects_cache', None):
            # En caso contenta relaciones foreanas se actualizan en la base de datos
            instance = self.get_object()
            serializer = self.get_serializer(instance)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance)

        return SuccessRestResponse(
            message=_('Object was updated successly'),
            data=serializer.data,
        )

    def destroy(self, request, *args, **kwargs):
        """Overwrite response when a object is deleted"""
        instance = self.get_object()
        try:
            instance.delete()
        except DatabaseError as ex:
            return ErrorRestResponse(str(ex))

        return SuccessRestResponse(
            message=_('Object was deleted successly'),
            status=status.HTTP_204_NO_CONTENT
        )


class LogModelViewSet(ModelViewSet):    
    def perform_create(self, serializer):
        """Overwrite de save method for log models"""
        serializer.save(usuario_creacion=self.request.user.id)