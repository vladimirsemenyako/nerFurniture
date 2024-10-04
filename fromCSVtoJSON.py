import csv
import json

# Открываем CSV файл
csv_file = 'Furniture.csv'
json_file = 'Furniture.json'

# Считываем данные из CSV и преобразуем в список словарей
with open(csv_file, 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    data = [row for row in reader]

# Записываем данные в JSON файл
with open(json_file, 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

print(f"Данные успешно сохранены в {json_file}")