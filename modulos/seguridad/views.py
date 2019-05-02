from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from agbc_servicio.views import APIView
from .serializers import UsuarioSerializer
from .utils import get_menu_user


class CurrentUserAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """Return current user info."""
        usuario = request.user
        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data)


class GetMenuAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """Return user menu"""
        menus = get_menu_user(request.user)
        return Response(menus)