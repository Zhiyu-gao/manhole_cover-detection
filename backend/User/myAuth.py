"""Custom JWT authentication for legacy user table."""

from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import User


class MyJWTAuthentication(JWTAuthentication):
    """Resolve JWT user id against custom `user` table."""

    def get_user(self, validated_token):
        user_id = validated_token.get("user_id")
        if user_id is None:
            raise AuthenticationFailed(_("Token格式错误"))

        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist as exc:
            raise AuthenticationFailed(_("用户不存在")) from exc
