from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UsuarioManager(BaseUserManager):
    """Manager de modelos de Usuario del modulo de seguridad"""
    def _create_user(self, username, email, persona_id, password, is_staff, is_superuser, **kwargs):
        """Funcion que realiza el registro de un usuario dentro del sistema"""
        now = timezone.now()
        if not email:
            raise ValueError(_('Debe Proporcionar un correo electronico'))
        email = self.normalize_email(email)
        user = self.model(
            username = username,
            persona_id = persona_id,
            email = email,
            is_staff = is_staff,
            is_active = True,
            is_superuser = is_superuser,
            last_login = now,
            fecha_registro = now,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, persona_id, password=None, **kwargs):
        """Funcion que realiza el registro de un usuario regular dentro del sistema"""
        return self._create_user(username, email, persona_id, password, False, False, **kwargs)
    
    def create_superuser(self, username, email, persona_id, password, **kwargs):
        """Funcion que realiza el registro de un usuario con privilegios de superusuario dentro del sistema"""
        return self._create_user(username, email, persona_id, password, True, True, **kwargs)


class Usuario(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('Nombre de Usuario'), max_length=50, unique = True)
    email = models.CharField(_('Correo Electrónico'), max_length=50, null = True, blank = True)
    persona_id = models.CharField(_('Nro. de Documento'), max_length = 25, unique = True)
    fecha_registro = models.DateTimeField(_('Fecha de Registro'), auto_now = True)
    is_active = models.BooleanField(_('Es Activo'), default = False)
    is_staff = models.BooleanField(_('Puede Logearse'), default = False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'persona_id']

    objects = UsuarioManager()


class Menu(models.Model):
    menu = models.CharField(_('Sidebar'), max_length=80)
    navbar = models.CharField(_('Navbar'), max_length=80)
    icon = models.CharField(_('Icono'), max_length=20)
    url_path = models.CharField(_('Url Path'), max_length=140)
    component = models.CharField(_('Componente'), max_length=50)
    parent = models.ForeignKey(
        'Menu',
        related_name='children',
        verbose_name=_('Padre'),
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    orden = models.SmallIntegerField(verbose_name=_('Orden'))

    def __str__(self):
        return self.menu


class UsuarioMenu(models.Model):
    usuario = models.ForeignKey('Usuario', related_name='+', on_delete=models.CASCADE)
    menu = models.ForeignKey('Menu', related_name='+', on_delete=models.CASCADE)