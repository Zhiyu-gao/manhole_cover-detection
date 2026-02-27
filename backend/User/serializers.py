"""Serializers for user authentication and user payloads."""

import hashlib

from rest_framework import exceptions, serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serialize user records."""

    class Meta:
        model = User
        fields = "__all__"


def _md5_digest(raw_text: str) -> str:
    return hashlib.md5(raw_text.encode("utf-8")).hexdigest()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom login serializer for legacy `user` table."""

    @classmethod
    def get_token(cls, user):
        return super().get_token(user)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if not username or not password:
            raise exceptions.ValidationError("username and password are required")

        encrypted_pwd = _md5_digest(password)

        try:
            user = User.objects.get(username=username, password=encrypted_pwd)
        except User.DoesNotExist as exc:
            raise exceptions.AuthenticationFailed("账号或密码错误") from exc

        refresh = self.get_token(user)
        return {
            "userId": user.id,
            "username": user.username,
            "token": str(refresh.access_token),
            "refresh": str(refresh),
        }
