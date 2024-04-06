from django.db import models
from django.utils import timezone

class HarvestData(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    weight = models.FloatField()
    irrigated = models.BooleanField()
    crop = models.CharField(max_length=200)
    date = models.DateField(default=timezone.now)  # Установил значение по умолчанию на текущую дату
