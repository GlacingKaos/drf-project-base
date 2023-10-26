from datetime import timedelta

import environ
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings

from .models import CustomUser

env = environ.Env()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["is_active"] = user.is_active
        token["tokenlifetime"] = str(timedelta(minutes=env.int("ACCESS_TOKEN_LIFETIME", 5)))

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data["is_active"] = self.user.is_active
        data["tokenlifetime"] = timedelta(minutes=env.int("ACCESS_TOKEN_LIFETIME", 5)).seconds

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=8, write_only=True)

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "password"]

    def validate(self, attrs):
        # first_name = attrs.get("first_name", "")
        # last_name = attrs.get("last_name", "")
        # email = attrs.get("email", "")
        # password = attrs.get("password", "")
        return attrs

    def create(self, validate_data):
        return CustomUser.objects.create_user(**validate_data)


class RecoverySerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        """
        Check that the email is correct.
        """
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este correo no es valido.")
        return value


class RegisterSendSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        """
        Check that the email is correct.
        """
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este correo no es valido.")
        user = CustomUser.objects.get(email=value)
        if user.is_verified:
            raise serializers.ValidationError("Este correo ya fue verificado.")
        return value


class TokenSerializer(serializers.Serializer):
    recovery_code = serializers.CharField(max_length=6, min_length=6)
    email = serializers.EmailField()


class ResetSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(max_length=68, min_length=8)
    confirm_password = serializers.CharField()

    def validate(self, attrs):
        password = attrs.get("password", "")
        confirm_password = attrs.get("confirm_password", "")
        if password != confirm_password:
            raise serializers.ValidationError("Las contraseñas no coinciden.")
        return attrs


class UserPasswordRecoverySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email"]


class UserShortSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ["id", "first_name", "last_name", "email", "full_name"]

    def get_full_name(self, obj):
        return obj.nombre_completo
