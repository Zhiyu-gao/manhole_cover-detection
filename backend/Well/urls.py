from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import FileUploadView, MonitorViewSet, UpdateAnnotationView, WellAPIView

router = DefaultRouter()
router.register(r"monitor", MonitorViewSet, basename="monitor")

urlpatterns = [
    path("wellApi", WellAPIView.as_view(), name="well-api"),
    path("upload", FileUploadView.as_view(), name="file-upload"),
    path("updateAnnotation", UpdateAnnotationView.as_view(), name="update-annotation"),
    path("", include(router.urls)),
]
