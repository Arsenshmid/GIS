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
import pandas as pd
from django.http import HttpResponse
import ee
from django.http import JsonResponse

def get_ee_data(request):
    # Инициализация Google Earth Engine
    ee.Initialize()

    # Загрузка набора данных о растительности
    collection = ee.ImageCollection('MODIS/006/MOD13A2').select('NDVI')

    # Указание временного диапазона
    collection = collection.filterDate('2018-01-01', '2018-12-31')

    # Указание области интереса
    aoi = ee.Geometry.Rectangle([-98.5, 39.0, -98.4, 39.1])

    # Усреднение значений NDVI по всем изображениям в коллекции
    average = collection.mean()

    # Применение маски для удаления областей без данных
    masked = average.updateMask(average)

    # Получение данных из Google Earth Engine
    url = masked.getThumbUrl({
        'region': aoi.toGeoJSONString(),
        'scale': 250,
        'min': 0,
        'max': 9000,
        'palette': ['blue', 'green', 'red']
    })

    # Возвращение данных в виде JSON-ответа
    return JsonResponse({'url': url})


    
def calculate_ndvi(request):
    # Загрузка данных из CSV
    data = pd.read_csv('synthetic_data.csv')

    # Проверка наличия необходимых столбцов
    if 'NIR' in data.columns and 'Red' in data.columns:
        # Расчет NDVI
        data['NDVI'] = (data['NIR'] - data['Red']) / (data['NIR'] + data['Red'])

        # Возвращение данных в виде HTTP-ответа
        response = HttpResponse(data.to_csv(index=False), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=ndvi.csv'

        return response
    else:
        return HttpResponse('Ошибка: в данных отсутствуют столбцы NIR и Red.')
    

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
    m = folium.Map(location=[62.0115, 129.0115], zoom_start=18, tiles='Mapbox Bright')  # Центральная точка области

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
