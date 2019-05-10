from django.utils.translation import ugettext_lazy as _
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from modulos.parametro.exceptions import ServicioAuthenticationFailed


class TokenAuthentication(BaseAuthentication):
    """"
    Simple authentication basada en Token.
    Pasar al Cliente el token key de Authorization
    HTTP header, incluido el TOKEN, por ejemplo:
    Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
    """

    keyword = 'Token'
    model = None

    def get_model(self):
        if self.model is not None:
            return self.model
        from rest_framework.authtoken.models import Token
        return Token
    
    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None
        
        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise ServicioAuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise ServicioAuthenticationFailed(msg)
        
        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise ServicioAuthenticationFailed(msg)
        
        return self.authenticate_credentials(token)
    
    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise ServicioAuthenticationFailed(_('Invalid token'))
        
        if not token.user.is_active:
            raise ServicioAuthenticationFailed(_('User inactive or deleted.'))
        
        return (token.user, token)
    
    def authenticate_header(self, request):
        return self.keyword