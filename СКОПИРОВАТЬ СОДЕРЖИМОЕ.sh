#!/bin/sh

# Создаем итоговый файл
touch final.txt

# Список файлов для копирования
files=("mysite/app/templates/home.html" "код для графика NDVI урожая в Якутске.txt" "mysite/загрузка в google earth engine.txt" "mysite/сгенерировать тестовые данные.py" "mysite/app/models.py" "mysite/app/views.py" "mysite/app/urls.py" "mysite/mysite/urls.py" "mysite/mysite/settings.py" "mysite/app/apps.py" "mysite/app/admin.py")

# Цикл по всем файлам
for file in "${files[@]}"
do
  # Проверяем, существует ли файл
  if [ -f "$file" ]; then
    echo "$file" >> final.txt # Записываем название файла
    cat "$file" >> final.txt # Записываем содержимое файла
    echo "" >> final.txt # Добавляем пустую строку для разделения
  else
    echo "Файл $file не найден"
  fi
done
