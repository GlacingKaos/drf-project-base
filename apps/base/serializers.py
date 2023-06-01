from django.contrib.auth.models import Group
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from apps.users.models import CustomUser


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "first_name", "last_name", "url", "email", "groups", "image"]


class UserMeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "first_name",
            "last_name",
            "url",
            "email",
            "groups",
            "is_verified",
            "image",
        ]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


class UserMePasswordSerializer(serializers.Serializer):
    actual_password = serializers.CharField()
    password = serializers.CharField(max_length=68, min_length=6)
    confirm_password = serializers.CharField()

    def validate(self, attrs):
        user = self.context["request"].user
        actual_password = attrs.get("actual_password", "")
        password = attrs.get("password", "")
        confirm_password = attrs.get("confirm_password", "")
        if password != confirm_password:
            raise serializers.ValidationError("Las contraseñas no coinciden.")
        if not user.check_password(actual_password):
            raise serializers.ValidationError("La contraseña actual es incorrecta.")
        return attrs
