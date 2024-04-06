import csv
import json
from collections import OrderedDict

# Загрузка CSV-файла
csv_file = 'synthetic_data.csv'

# Создание пустого списка для хранения данных
features = []

# Чтение CSV-файла
with open(csv_file, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Создание объекта Feature для каждой строки
        feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [float(row['longitude']), float(row['latitude'])]
            },
            'properties': {
                'weight': int(row['weight']),
                'irrigated': row['irrigated'],
                'crop': row['crop']
            }
        }
        features.append(feature)

# Создание GeoJSON-объекта
geojson = {
    'type': 'FeatureCollection',
    'features': features
}

# Сохранение GeoJSON в файл
with open('output.geojson', 'w') as outfile:
    json.dump(geojson, outfile)

print("GeoJSON файл успешно создан: output.geojson")
