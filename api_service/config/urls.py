from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import IndicatorViewSet, DataViewSet, get_map_geojson

router = DefaultRouter()
router.register(r'indicators', IndicatorViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/indicators/<int:indicator_pk>/data/', DataViewSet.as_view({'get': 'list'}), name='indicator-data'),
    path('api/maps/<str:filename>/', get_map_geojson, name='get-map'),
]