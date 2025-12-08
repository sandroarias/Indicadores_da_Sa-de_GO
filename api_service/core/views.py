import os
import json
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Indicator, IndicatorRecord
from .serializers import IndicatorSerializer, IndicatorRecordSerializer

class IndicatorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Indicator.objects.all()
    serializer_class = IndicatorSerializer

class DataViewSet(viewsets.ViewSet):
    def list(self, request, indicator_pk=None):
        queryset = IndicatorRecord.objects.filter(indicator_id=indicator_pk)
        
        filters = {}
        for key, value in request.query_params.items():
            filters[f'data__{key}'] = value

        if filters:
            queryset = queryset.filter(**filters)

        serializer = IndicatorRecordSerializer(queryset[:5000], many=True)
        return Response(serializer.data)
    
def get_map_geojson(request, filename):
    
    file_path = f'/app/data_source/maps/{filename}.json'
    
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Mapa não encontrado'}, status=404)