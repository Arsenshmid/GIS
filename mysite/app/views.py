import folium
from django.shortcuts import render
import pandas as pd
from .models import HarvestData
import numpy as np
import matplotlib.pyplot as plt
from django.shortcuts import render
from .models import HarvestData
from io import BytesIO
import base64
from shapely.geometry import Polygon
import geopandas as gpd

def chart_view(request):
    # Получение данных из модели Django
    data = HarvestData.objects.all()

    # Создание списков для хранения данных
    dates = []
    weights = []

    # Заполнение списков данными
    for point in data:
        dates.append(point.date)
        weights.append(point.weight)

    # Создание графика
    plt.figure(figsize=(10, 5))
    plt.plot(dates, weights)
    plt.title('NDVI time series for a single pixel')
    plt.xlabel('Date')
    plt.ylabel('NDVI')

    # Сохранение графика в PNG
    buf = BytesIO()
    plt.savefig(buf, format='png')
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    buf.close()

    return render(request, 'chart.html', {'image_base64': image_base64})

def load_data():
    # Чтение данных из CSV-файла
    df = pd.read_csv('synthetic_data.csv')

    # Загрузка данных в модель Django
    for index, row in df.iterrows():
        data = HarvestData(latitude=row['latitude'], longitude=row['longitude'], weight=row['weight'], irrigated=row['irrigated'], crop=row['crop'])
        data.save()

def map_view(request):
    # Загрузка данных
    load_data()

    # Создание карты
    m = folium.Map(location=[62.0115, 129.0115], zoom_start=18)  # Центральная точка области

    # Создание списка координат всех точек
    coords = [(data.latitude, data.longitude) for data in HarvestData.objects.all()]

    # Создание полигона по границе крайних точек
    polygon = Polygon(coords)

    # Создание GeoDataFrame с полигона
    gdf = gpd.GeoDataFrame([1], geometry=[polygon], crs="EPSG:4326")

    # Добавление полигона на карту
    folium.GeoJson(gdf).add_to(m)

    # Градиентная окраска области на карте
    # (это требует дополнительной работы, так как Folium не поддерживает градиентную окраску напрямую)

    # Добавление данных из модели Django на карту
    for data in HarvestData.objects.all():
        # Выбор цвета в зависимости от веса урожая
        if data.weight < 30:
            color = 'red'
        elif data.weight < 60:
            color = 'yellow'
        else:
            color = 'green'

        # Добавление маркера на карту
        folium.CircleMarker([data.latitude, data.longitude], radius=10, popup=f'Weight: {data.weight}', color=color, fill=True, fill_color=color).add_to(m)

    # Генерация HTML-строки с картой
    m = m._repr_html_()

    return render(request, 'home.html', {'map': m})
