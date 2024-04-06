import pandas as pd
import numpy as np

# Создаем пустой DataFrame
df = pd.DataFrame(columns=['latitude', 'longitude', 'weight', 'irrigated', 'crop'])

# Задаем границы области внутри Якутска (примерно 200 метров)
min_lat, max_lat = 62.01, 62.012
min_lon, max_lon = 129.01, 129.012

# Задаем шаг для генерации точек
step = 0.00027  # примерно 30 метров

# Заполняем DataFrame данными
i = 0
for lat in np.arange(min_lat, max_lat, step):
    for lon in np.arange(min_lon, max_lon, step):
        weight = np.random.randint(0, 1001)  # вес урожая в кг (от 0 до 1000 кг)
        irrigated = np.random.choice([True, False])  # орошалась ли область
        crop = np.random.choice(['wheat', 'corn', 'soy'])  # какая культура была посажена

        df.loc[i] = [lat, lon, weight, irrigated, crop]
        i += 1

# Сохраняем DataFrame в файл CSV
df.to_csv('synthetic_data.csv', index=False)
