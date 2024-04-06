from django.db import models

class HarvestData(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    weight = models.FloatField()
    irrigated = models.BooleanField()
    crop = models.CharField(max_length=50)


