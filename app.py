import os
import requests
import uuid
import json
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template,request
app = Flask(__name__)
@app.route('/index/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

    # Прочтение значения из формы
    original_text = request.form['text']
    target_language = request.form['language']

    # Загрузка значения .env
    key = os.environ['KEY']
    endpoint = os.environ['ENDPOINT']
    location = os.environ['LOCATION']

    # Указываем, что хотим перевести API
    # Целевой язык

    path = '/translate?api-version=3.0'

    # Добавление параметра целевого языка
    target_language_parameter = '&to=' + target_language

    # Создание полного URL
    constructed_url = endpoint + path + target_language_parameter

    # Настройка информации в заголовке
    # Ключ подписки
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # Создание тела запроса с текстом
    # Перевод
    body = [{'text': original_text}]

    # Звонок post
    translator_request = requests.post(
        constructed_url, headers=headers, json=body)

    # Получение ответа json
    translator_response = translator_request.json()

    translated_text = translator_response[0]['translations'][0]['text']

    # Вызвать шаблон рендера, передав переведенный текст
    # Исходный текст и целевой язык для шаблона
    return render_template(
        'results.html',
        translated_text=translated_text,
        original_text=original_text,
        target_language=target_language
    )
