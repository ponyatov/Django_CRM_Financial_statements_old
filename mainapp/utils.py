import os
import json
import re

import requests
from dotenv import load_dotenv

from django.contrib import messages


load_dotenv()

URL = 'https://api.fintablo.ru/v1/'
TOKEN = os.getenv('API_KEY_FIN-TABLO')
HEADERS = {'Authorization': f'Bearer {TOKEN}'}

URL_YANDEX = 'https://cloud-api.yandex.net/v1/disk/resources/upload/'
YANDEX_TOKEN = os.getenv('API_YANDEX_DISK')
HEADERS_YANDEX = {'Authorization': f'OAuth {YANDEX_TOKEN}'}


# REQUEST GET LIST
def get_data_from_api(endpoint):
    """
    Динамическая функция для получения
    :param endpoint:
    :return: moneybag, deal, partner, category
    """
    url_pattern = URL + endpoint
    response = requests.get(url_pattern, headers=HEADERS)

    if response.status_code == 200:
        data = response.json()

        # print(data)
        return [{'id': item['id'], 'name': item['name']} for item in data['items']]
    else:
        print(f"Ошибка при получении данных: {response.status_code}")


def get_list_money():
    return get_data_from_api('moneybag')


# print(get_list_money())


def get_list_deal():
    return get_data_from_api('deal')


# print(get_list_deal())


def get_list_counterparty():
    return get_data_from_api('partner')


def get_list_articles():
    return get_data_from_api('category')


# print(get_list_articles())


# ======================================================================================================================
# REQUEST POST
def add_outcome(request, form, moneybag_id, description):
    payload = {
        "value": form.cleaned_data['value'],
        "moneybagId": moneybag_id,
        "group": "outcome",
        "description": description,
        "date": "15.04.2024",
    }
    if form.cleaned_data.get('undisclosed'):
        payload["categoryId"] = form.cleaned_data['undisclosed']

    if form.cleaned_data.get('deal_name'):
        payload["dealId"] = form.cleaned_data['deal_name']

    if form.cleaned_data.get('counterparty'):
        payload["partnerId"] = form.cleaned_data['counterparty']

    url_pattern = URL + 'transaction'
    print(payload)
    try:
        response = requests.post(url_pattern, json=payload, headers=HEADERS)
        response.raise_for_status()
        print('Операция добавлена')

    except requests.exceptions.RequestException as e:
        print('Произошла ошибка при выполнении запроса:', e)
        messages.error(request, 'Произошла ошибка при выполнении запроса. Пожалуйста, попробуйте еще раз.')


# POST IMAGE TO YANDEX_DISK
def disk_resources_upload(file_path, dir_path=''):
    params = {
        'path': os.path.join(dir_path, os.path.basename(file_path)),
        'overwrite': 'true'
    }
    url_query = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
    result_query = send_query_ya_disk(url_query, params)

    if 'error' not in result_query:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response_upload = requests.put(result_query['href'], files=files)
            http_code = response_upload.status_code
        return http_code
    else:
        return result_query['message']


def send_query_ya_disk(url, params):
    response = requests.get(url, params=params, headers={'Authorization': f'OAuth {YANDEX_TOKEN}'})
    return response.json() if response.ok else {'error': 'Failed to get upload URL'}