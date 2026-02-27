from django.db import models


class Well(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    file_name = models.CharField(max_length=255, blank=True, null=True)
    image_id = models.CharField(max_length=255, blank=True, null=True)
    width = models.CharField(max_length=255, blank=True, null=True)
    height = models.CharField(max_length=255, blank=True, null=True)
    bbox = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    area = models.CharField(max_length=255, blank=True, null=True)
    time = models.CharField(max_length=255, blank=True, null=True)
    user = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "well"


class Monitor(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    time = models.CharField(max_length=255, blank=True, null=True)
    position = models.CharField(max_length=255, blank=True, null=True)
    img = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    img2 = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "monitor"
