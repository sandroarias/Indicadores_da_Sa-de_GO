from django.contrib import admin
from django.urls import path
from web import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/<str:indicator_id>/', views.dashboard_view, name='dashboard'),
    
    path('api/indicators/', views.get_all_indicators, name='all_indicators'), 
    
    path('api/indicators/<str:indicator_id>/metadata/', views.get_indicator_metadata, name='indicator_metadata'),
    path('api/indicators/<str:indicator_id>/data/', views.get_indicator_data, name='indicator_data'),
    path('api/maps/<str:map_id>/', views.get_map_data, name='map_data'),
    path('api/indicators/<str:indicator_id>/filters/', views.get_available_filters, name='available_filters'),
]