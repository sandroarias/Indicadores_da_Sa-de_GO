import requests
from django.shortcuts import render
from django.http import JsonResponse
import json

API_BASE_URL = "http://api:8000/api"

def index(request):
    try:
        response = requests.get(f"{API_BASE_URL}/indicators/")
        indicators = response.json()
    except Exception as e:
        print(f"Erro ao buscar indicadores: {e}")
        indicators = []
    
    return render(request, 'index.html', {'indicators': indicators})

def dashboard_view(request, indicator_id):

    return render(request, 'dashboard.html', {
        'indicator_id': indicator_id
    })

def get_indicator_metadata(request, indicator_id):
    try:
        response = requests.get(f"{API_BASE_URL}/indicators/{indicator_id}/")
        return JsonResponse(response.json())
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_indicator_data(request, indicator_id):

    try:
        # Pega todos os parâmetros de filtro da requisição
        params = request.GET.dict()
        
        data_url = f"{API_BASE_URL}/indicators/{indicator_id}/data/"
        response = requests.get(data_url, params=params)
        
        return JsonResponse(response.json(), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_map_data(request, map_id):

    try:
        response = requests.get(f"{API_BASE_URL}/maps/{map_id}/")
        return JsonResponse(response.json())
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_available_filters(request, indicator_id):

    try:
        data_url = f"{API_BASE_URL}/indicators/{indicator_id}/data/"
        response = requests.get(data_url)
        data = response.json()
        
        if not data:
            return JsonResponse({'filters': {}})
        
        filters = {}
        keys = data[0].get('data', {}).keys()
        
        for key in keys:
            unique_values = sorted(list(set(
                item['data'][key] for item in data 
                if item.get('data', {}).get(key) is not None
            )))
            filters[key] = unique_values
        
        return JsonResponse({'filters': filters})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

def get_all_indicators(request):
    try:
        response = requests.get(f"{API_BASE_URL}/indicators/")
        return JsonResponse(response.json(), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)