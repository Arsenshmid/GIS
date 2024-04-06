import folium
from django.shortcuts import render
import pandas as pd
from .models import HarvestData
import numpy as np

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
    m = folium.Map(location=[62.011, 129.011], zoom_start=15)  # Центральная точка области

    # Добавление данных из модели Django на карту
    for data in HarvestData.objects.all():
        # Выбор цвета в зависимости от веса урожая
        if data.weight < 333:
            color = 'red'
        elif data.weight < 666:
            color = 'yellow'
        else:
            color = 'green'

        # Добавление маркера на карту
        folium.CircleMarker([data.latitude, data.longitude], radius=10, popup=f'Weight: {data.weight}', color=color, fill=True, fill_color=color).add_to(m)

    # Генерация HTML-строки с картой
    m = m._repr_html_()

    return render(request, 'home.html', {'map': m})
