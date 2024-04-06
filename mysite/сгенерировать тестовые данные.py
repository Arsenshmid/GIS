import pandas as pd
import numpy as np

# Создаем пустой DataFrame
df = pd.DataFrame(columns=['latitude', 'longitude', 'weight', 'irrigated', 'crop'])

# Задаем границы области внутри Якутска (примерно 38x38 метров)
min_lat, max_lat = 62.011, 62.0115  # Уменьшаем границы
min_lon, max_lon = 129.011, 129.0115  # Уменьшаем границы

# Задаем шаг для генерации точек
step = 0.00005  # Увеличиваем шаг до примерно 50 метров

# Заполняем DataFrame данными
prev_weight = np.random.randint(0, 1001)  # вес урожая в кг (от 0 до 1000 кг)
for lat in np.arange(min_lat, max_lat, step):
    for lon in np.arange(min_lon, max_lon, step):
        weight = prev_weight + np.random.randint(-50, 51)  # вес урожая в кг (от 0 до 1000 кг)
        weight = max(0, weight)  # убедимся, что вес не станет отрицательным
        weight = min(1000, weight)  # убедимся, что вес не превысит 1000
        prev_weight = weight
        irrigated = np.random.choice([True, False])  # орошалась ли область
        crop = np.random.choice(['wheat', 'corn', 'soy'])  # какая культура была посажена

        new_row = pd.DataFrame([[lat, lon, weight, irrigated, crop]], columns=df.columns)
        df = pd.concat([df, new_row], ignore_index=True)

# Сохраняем DataFrame в файл CSV
df.to_csv('synthetic_data.csv', index=False)
