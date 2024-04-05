import folium
from django.shortcuts import render
import geopandas as gpd
import pandas as pd
from .models import HarvestData
import folium
from django.shortcuts import render
from .models import HarvestData

def load_data():
    # Чтение данных из CSV-файла
    df = pd.read_csv('synthetic_data.csv')

    # Загрузка данных в модель Django
    for index, row in df.iterrows():
        data = HarvestData(latitude=row['latitude'], longitude=row['longitude'], weight=row['weight'], irrigated=row['irrigated'], crop=row['crop'])
        data.save()

def home(request):
    # Загрузка данных
    load_data()

    # Создание карты
    m = folium.Map(location=[62.035452, 129.675475], zoom_start=13)

    # Добавление данных из модели Django на карту
    for data in HarvestData.objects.all():
        # Выбор цвета в зависимости от веса урожая
        if data.weight < 60:
            color = 'red'
        elif data.weight < 70:
            color = 'yellow'
        else:
            color = 'green'

        # Добавление маркера на карту
        folium.Marker([data.latitude, data.longitude], popup=f'Weight: {data.weight}', icon=folium.Icon(color=color)).add_to(m)

    # Генерация HTML-строки с картой
    m = m._repr_html_()

    return render(request, 'home.html', {'map': m})





