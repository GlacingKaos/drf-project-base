"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import environ
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

from apps.base import views
from apps.users.views import TokenObtainPairNewView, TokenRefreshNewView

env = environ.Env()


schema_view = get_schema_view(
    openapi.Info(
        title="{} API".format(env.str("API_NAME", "api").upper()),
        default_version="v1.0.0",
        description="API description, Para usar esta api se necesita de un token(JWT), se debe mandar en los headers como 'Authorization':'Barer my_api_token'",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = routers.DefaultRouter()

router.register(r"users", views.UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("admin/", admin.site.urls),
    path("v1/auth/me/", views.MeAPIView.as_view(), name="auth-get-me"),
    path("v1/auth/token/", TokenObtainPairNewView.as_view(), name="token_obtain_pair"),
    path("v1/auth/token/refresh/", TokenRefreshNewView.as_view(), name="token_refresh"),
    path("v1/", include(router.urls)),
    path("v1/users/me/password/", views.UserMePasswordView.as_view(), name="me-password"),
    path("v1/ping/", views.PingAPIView.as_view()),
    path("v1-auth/", include("rest_framework.urls", namespace="rest_framework")),
    # API-DOC
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
