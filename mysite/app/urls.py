from django.urls import path
from . import views
from .views import calculate_ndvi, chart_view, load_data, map_view

urlpatterns = [
    path('', views.map_view, name='map'),
    path('chart/', views.chart_view, name='chart'),
    path('calculate_ndvi/', calculate_ndvi, name='calculate_ndvi'),
    path('chart_view/', chart_view, name='chart_view'),
    path('load_data/', load_data, name='load_data'),
    path('map_view/', map_view, name='map_view'),
]
