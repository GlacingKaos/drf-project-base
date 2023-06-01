
import environ

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import (
    MyTokenObtainPairSerializer,

)

env = environ.Env()


class TokenRefreshNewView(TokenRefreshView):
    pass


class TokenObtainPairNewView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

