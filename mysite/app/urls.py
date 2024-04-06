from django.urls import path
from . import views
# your_app/urls.py
from django.urls import path
from .views import get_ee_data
from .views import calculate_ndvi, chart_view, load_data, map_view, get_ee_data


urlpatterns = [
    path('', views.map_view, name='map'),
    path('chart/', views.chart_view, name='chart'),
    path('ee-data/', get_ee_data, name='get_ee_data'),
    path('calculate_ndvi/', calculate_ndvi, name='calculate_ndvi'),
    path('chart_view/', chart_view, name='chart_view'),
    path('load_data/', load_data, name='load_data'),
    path('map_view/', map_view, name='map_view'),
    path('get_ee_data/', get_ee_data, name='get_ee_data'),
]