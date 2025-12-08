from rest_framework import serializers
from .models import Indicator, IndicatorRecord

class IndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicator
        fields = '__all__'

class IndicatorRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndicatorRecord
        fields = ['data']