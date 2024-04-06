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
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
from django.shortcuts import render
from io import BytesIO
import base64

import pandas as pd
import matplotlib.pyplot as plt
from django.shortcuts import render
from io import BytesIO
import base64
import pandas as pd
import matplotlib.pyplot as plt
from django.shortcuts import render
from io import BytesIO
import base64

def chart_view(request):
    period = request.GET.get('period', 'months')  # Получаем выбранный период, если не выбран, то по умолчанию 'months'

    # Считываем данные из файла ee-chart.csv
    data_df = pd.read_csv('ee-chart.csv')

    # Преобразуем столбец 'system:time_start' в формат datetime
    data_df['system:time_start'] = pd.to_datetime(data_df['system:time_start'])

    # Удаляем строки с отсутствующими значениями NDVI
    data_df = data_df.dropna(subset=['0'])

    # Преобразуем значения NDVI в числовой формат
    data_df['0'] = pd.to_numeric(data_df['0'], errors='coerce')

    if period == 'months':
        # Группируем данные по месяцам и вычисляем среднее значение NDVI
        data_df['year_month'] = data_df['system:time_start'].dt.to_period('M')
        grouped_data = data_df.groupby('year_month').mean()
        title = 'Средний NDVI по месяцам'
        x_label = 'Месяц'
    elif period == 'years':
        # Группируем данные по годам и вычисляем среднее значение NDVI
        data_df['year'] = data_df['system:time_start'].dt.year
        grouped_data = data_df.groupby('year').mean()
        title = 'Средний NDVI по годам'
        x_label = 'Год'
    elif period == 'both':
        # Группируем данные одновременно по годам и месяцам и вычисляем среднее значение NDVI
        data_df['year_month'] = data_df['system:time_start'].dt.strftime('%Y-%m')
        grouped_data = data_df.groupby('year_month').mean()
        title = 'Средний NDVI по месяцам и годам'
        x_label = 'Месяц и год'

    # Создаем график
    plt.figure(figsize=(10, 5))
    plt.plot(grouped_data.index.astype(str), grouped_data['0'])  # Преобразуем периоды в строки
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel('Средний NDVI')

    # Сохраняем график в PNG
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
    

