from django.db import models
from django.contrib.postgres.indexes import GinIndex

# Modelo para representar um indicador.
class Indicator(models.Model):
    uid = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True)
    unit = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return self.title

# Modelo para armazenar registros associados a um indicador.
class IndicatorRecord(models.Model):
    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE, related_name='records')
    
    data = models.JSONField()

    class Meta:
        indexes = [
            GinIndex(fields=['data'], name='json_data_gin_idx'), 
        ]