import pandas as pd
import numpy as np

# Создаем пустой DataFrame
df = pd.DataFrame(columns=['latitude', 'longitude', 'weight', 'irrigated', 'crop'])

# Заполняем DataFrame случайными данными
for i in range(1000):  # создаем 1000 точек данных
    lat = 62 + np.random.rand()  # широта
    lon = 129 + np.random.rand()  # долгота
    weight = np.random.randint(50, 100)  # вес урожая в кг
    irrigated = np.random.choice([True, False])  # орошалась ли область
    crop = np.random.choice(['wheat', 'corn', 'soy'])  # какая культура была посажена

    df.loc[i] = [lat, lon, weight, irrigated, crop]

# Сохраняем DataFrame в файл CSV
df.to_csv('synthetic_data.csv', index=False)
