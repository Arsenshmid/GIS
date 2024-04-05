import folium
from django.shortcuts import render
import geopandas as gpd

def home(request):
    # Чтение файла .gpkg
    gdf = gpd.read_file('C:/Users/apce1/Desktop/данные для карты/data/airport-polygon.gpkg')

    # Создание карты
    m = folium.Map(location=[62.035452, 129.675475], zoom_start=13)

    # Добавление данных GeoDataFrame в карту
    for _, r in gdf.iterrows():
        # Преобразование каждой геометрии в данные GeoJSON
        sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.001)
        geo_j = sim_geo.to_json()
        geo_j = folium.GeoJson(data=geo_j,
                               style_function=lambda x: {'fillColor': 'orange'})
        
        # Добавление данных GeoJSON в карту
        geo_j.add_to(m)

    # Генерация HTML-строки с картой
    m = m._repr_html_()

    return render(request, 'home.html', {'map': m})
