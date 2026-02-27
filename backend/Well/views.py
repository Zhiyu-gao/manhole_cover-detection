"""API views for well data, upload inference, and monitor records."""

from __future__ import annotations

import logging
import uuid
from pathlib import Path

from django.conf import settings
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .inference import InferenceError, predict_image
from .models import Monitor, Well
from .serializers import MonitorSerializer, WellSerializer

LOGGER = logging.getLogger(__name__)


class WellAPIView(APIView):
    """Return paginated well records."""

    permission_classes = [AllowAny]

    def get(self, request):
        try:
            page = max(int(request.query_params.get("page", 1)), 1)
            page_size = min(max(int(request.query_params.get("page_size", 10)), 1), 100)
        except ValueError:
            return Response(
                {"error": "page and page_size must be integers"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        start = (page - 1) * page_size
        end = start + page_size

        queryset = Well.objects.all().order_by("id")
        total = queryset.count()
        records = queryset[start:end]

        return Response(
            {
                "wellData": WellSerializer(records, many=True).data,
                "total": total,
                "page": page,
                "page_size": page_size,
            }
        )


class FileUploadView(APIView):
    """Upload image and return model inference result."""

    permission_classes = [AllowAny]

    def post(self, request):
        uploaded_file = request.FILES.get("upload_file")
        if uploaded_file is None:
            return Response(
                {"error": "upload_file is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        file_extension = Path(uploaded_file.name).suffix.lower() or ".jpg"
        if file_extension not in {".jpg", ".jpeg", ".png", ".bmp", ".webp"}:
            return Response(
                {"error": "Unsupported file type"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        filename = f"{uuid.uuid4().hex}{file_extension}"
        static_root = Path(settings.STATIC_ROOT)
        static_root.mkdir(parents=True, exist_ok=True)
        file_path = static_root / filename

        try:
            with file_path.open("wb") as output:
                for chunk in uploaded_file.chunks():
                    output.write(chunk)

            predicted_category = predict_image(file_path)
        except InferenceError as exc:
            LOGGER.warning("Inference failed for %s: %s", filename, exc)
            if file_path.exists():
                file_path.unlink(missing_ok=True)
            return Response(
                {"error": "Inference failed", "detail": str(exc)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as exc:  # pragma: no cover
            LOGGER.exception("Upload failed: %s", exc)
            if file_path.exists():
                file_path.unlink(missing_ok=True)
            return Response(
                {"error": "Upload failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response({"path": f"/static/{filename}", "label": predicted_category})


class UpdateAnnotationView(APIView):
    """Update category/bbox annotation for a well record."""

    permission_classes = [AllowAny]

    def put(self, request):
        well_id = request.data.get("id")
        if not well_id:
            return Response(
                {"error": "id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            well = Well.objects.get(id=well_id)
        except Well.DoesNotExist:
            return Response(
                {"error": "Record not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = WellSerializer(well, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MonitorViewSet(ModelViewSet):
    """CRUD endpoints for monitor records."""

    permission_classes = [AllowAny]
    queryset = Monitor.objects.all().order_by("-time")
    serializer_class = MonitorSerializer
