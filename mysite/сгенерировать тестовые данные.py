import pandas as pd
import numpy as np

# Создаем пустой DataFrame
df = pd.DataFrame(columns=['latitude', 'longitude', 'weight', 'irrigated', 'crop'])

# Задаем границы области внутри Якутска (примерно 2 км)
min_lat, max_lat = 62, 62.02
min_lon, max_lon = 129, 129.02

# Задаем шаг для генерации точек
step = 0.00018  # примерно 20 метров

# Заполняем DataFrame данными
i = 0
for lat in np.arange(min_lat, max_lat, step):
    for lon in np.arange(min_lon, max_lon, step):
        weight = np.random.randint(56, 66)  # вес урожая в кг (ближе к предыдущему результату)
        irrigated = np.random.choice([True, False])  # орошалась ли область
        crop = np.random.choice(['wheat', 'corn', 'soy'])  # какая культура была посажена

        df.loc[i] = [lat, lon, weight, irrigated, crop]
        i += 1

# Сохраняем DataFrame в файл CSV
df.to_csv('synthetic_data.csv', index=False)
