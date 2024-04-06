import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Считываем данные из CSV файла
df = pd.read_csv('ee-chart.csv', parse_dates=['system:time_start'], dayfirst=True)

# Создаем график
fig, ax = plt.subplots()
ax.plot(df['system:time_start'], df['0'], label='NDVI', color='b')
ax.set_title('NDVI временной ряд')
ax.set_xlabel('Дата')
ax.set_ylabel('NDVI')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

# Сохраняем график в файл chart.html
plt.savefig('chart.html')

print("График сохранен в файл chart.html")
