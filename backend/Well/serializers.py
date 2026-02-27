"""Serializers for well and monitor models."""

from rest_framework import serializers

from .models import Monitor, Well


class WellSerializer(serializers.ModelSerializer):
    wellurl = serializers.SerializerMethodField()

    class Meta:
        model = Well
        fields = ("id", "wellurl", "bbox", "user", "category", "image_id")

    def get_wellurl(self, obj):
        return f"/static/{obj.image_id}.jpg" if obj.image_id else ""


class MonitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monitor
        fields = "__all__"
