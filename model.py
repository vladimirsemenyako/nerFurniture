import json
import spacy
from spacy.tokens import DocBin
from spacy.util import filter_spans
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup

# Загрузка модели en_core_web_lg
nlp = spacy.load('en_core_web_lg')

# Загрузка тренировочных данных
with open('datasetFurniture.json', 'r') as f:
    data = json.load(f)

training_data = []

# Формируем тренировочные данные из JSON
for elem in data:
    temp_dict = {}
    temp_dict['text'] = elem['name']
    temp_dict['entities'] = []
    for label in elem['label']:
        start = label['start']
        end = label['end']
        label = label['labels'][0].upper()
        temp_dict['entities'].append((start, end, label))
    training_data.append(temp_dict)

# Создание пустой модели Spacy
nlp = spacy.blank('en')

# Подготовка для хранения документов
doc_bin = DocBin()

# Преобразование тренировочных данных в документы Spacy
for training_example in tqdm(training_data):
    text = training_example['text']
    labels = training_example['entities']
    doc = nlp.make_doc(text)
    ents = []
    for start, end, label in labels:
        span = doc.char_span(start, end, label=label, alignment_mode='contract')
        if span is None:
            continue
        else:
            ents.append(span)
    filtered_ents = filter_spans(ents)
    doc.ents = filtered_ents
    doc_bin.add(doc)

# Сохранение в бинарный формат
doc_bin.to_disk("train.spacy")

# Загрузка обученной модели NER
nlp_ner = spacy.load("model-best")

# Функция для парсинга веб-сайта и извлечения сущностей типа PRODUCT
def parse_website(url):
    # 1. Загрузить HTML-контент с сайта
    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.text
    else:
        print(f"Ошибка при загрузке страницы: {response.status_code}")
        return None

    # 2. Извлечь текст из HTML с помощью BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    texts = soup.stripped_strings  # Извлекаем все текстовые строки
    full_text = " ".join(texts)  # Собираем их в один текст

    # 3. Применить модель NER для извлечения сущностей
    doc = nlp_ner(full_text)

    # 4. Найти все сущности типа PRODUCT и удалить дубликаты
    products = [ent.text for ent in doc.ents if ent.label_ == "PRODUCT"]
    unique_products = list(set(products))  # Удаление дубликатов

    return unique_products