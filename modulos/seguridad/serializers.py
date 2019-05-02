from rest_framework import serializers
from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = (
            'username',
            'email',
            'persona_id',
            'fecha_registro',
            'is_active',
            'is_staff'
        )