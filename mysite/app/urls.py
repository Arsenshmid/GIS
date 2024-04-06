from django.urls import path
from . import views

urlpatterns = [
    path('', views.map_view, name='map'),
    path('chart/', views.chart_view, name='chart'),
]