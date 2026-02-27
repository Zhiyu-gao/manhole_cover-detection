from django.urls import path

from .views import JwtLoginView, TestView

urlpatterns = [
    path("jwtLogin", JwtLoginView.as_view(), name="jwt-login"),
    path("test", TestView.as_view(), name="test"),
]
