"""Views for user login and auth test endpoint."""

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import MyTokenObtainPairSerializer, UserSerializer


class JwtLoginView(APIView):
    """Issue JWT for username/password."""

    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        serializer = MyTokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


class TestView(APIView):
    """Return current user details if authenticated."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"user_info": UserSerializer(request.user).data})
