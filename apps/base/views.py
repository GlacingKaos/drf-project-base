import environ
from django.contrib.auth.models import Group
from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.base.serializers import GroupSerializer, UserMePasswordSerializer, UserMeSerializer, UserSerializer
from apps.users.models import CustomUser

env = environ.Env()


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = CustomUser.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserMePasswordView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserMePasswordSerializer

    def patch(self, request):
        user = CustomUser.objects.get(pk=request.user.pk)
        pass_data = request.data
        serializer = self.serializer_class(data=pass_data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        user.set_password(validated_data["password"])
        user.save()
        return Response(UserMeSerializer(user, context={"request": request}).data)


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class PingAPIView(APIView):
    """
    View to Ping in the system.
    """

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        """
        Return info api.
        """
        return Response(
            {
                "version": env.str("API_VERSION", "v1.0.0"),
                "default_format": env.str("API_DEFAULT_FORMAT", "json"),
                "name": env.str("API_NAME", "API"),
            }
        )


class MeAPIView(APIView):
    """
    View to Me in the system.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        queryset = CustomUser.objects.get(pk=request.user.pk)
        return Response(UserMeSerializer(queryset, context={"request": request}).data)
