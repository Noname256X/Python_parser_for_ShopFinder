import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import json
import os
import re
from Parser import *
from scroll_page import dynamic_scroll
import random
from selenium.webdriver.common.action_chains import ActionChains
from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import requests


app = Flask(__name__)
CORS(app)

@app.route('/parse', methods=['POST'])

@app.route('/status')
def status():
    # Здесь можно добавить логику проверки занятости сервера
    return jsonify({"status": "ready"})

def parse_marketplace():
    data = request.json
    query = data['query']
    marketplace = data['marketplace']
    ip = data['ip']

    # Запускаем парсинг в отдельном потоке
    thread = threading.Thread(
        target=run_parsing,
        args=(query, marketplace, ip)
    )
    thread.start()

    return jsonify({"status": "started"})


def run_parsing(query, marketplace, ip):
    # Отправляем статус на REST API
    def send_status(message):
        requests.post(
            'http://nodejs-api:3000/api/status',
            json={'ip': ip, 'message': message}
        )

    # Вызываем соответствующую функцию парсинга
    if marketplace == 'Ozon':
        send_status(f"Ozon: Начало парсинга для '{query}'")
        get_products_links_html_Ozon(query, ip)
    elif marketplace == 'Wildberries':
        send_status(f"Wildberries: Начало парсинга для '{query}'")
        get_products_links_WB(query, ip)
    elif marketplace == 'YandexMarket':
        send_status(f"YandexMarket: Начало парсинга для '{query}'")
        get_products_links_YandexMarket(query, ip)
    elif marketplace == 'MagnitMarket':
        send_status(f"MagnitMarket: Начало парсинга для '{query}'")
        get_products_links_MagnitMarket(query, ip)
    elif marketplace == 'DNS':
        send_status(f"DNS: Начало парсинга для '{query}'")
        get_products_links_DNS(query, ip)
    elif marketplace == 'Citilink':
        send_status(f"Citilink: Начало парсинга для '{query}'")
        get_products_links_Citilink(query, ip)
    elif marketplace == 'M_Video':
        send_status(f"M_Video: Начало парсинга для '{query}'")
        get_products_links_M_Video(query, ip)
    elif marketplace == 'Aliexpress':
        send_status(f"Aliexpress: Начало парсинга для '{query}'")
        get_products_links_Aliexpress(query, ip)
    elif marketplace == 'Joom':
        send_status(f"Joom: Начало парсинга для '{query}'")
        get_products_links_Joom(query, ip)
    elif marketplace == 'Shop_mts':
        send_status(f"Shop_mts: Начало парсинга для '{query}'")
        get_products_links_Shop_mts(query, ip)
    elif marketplace == 'Technopark':
        send_status(f"Technopark: Начало парсинга для '{query}'")
        get_products_links_Technopark(query, ip)
    elif marketplace == 'Lamoda':
        send_status(f"Lamoda: Начало парсинга для '{query}'")
        get_products_links_Lamoda(query, ip)


def get_products_links_html_Ozon(item_name, user_ip):
    driver = uc.Chrome(version_main=135)
    driver.implicitly_wait(10)

    try:
        text_processing = item_name.replace(' ', '+')
        driver.get(f'https://www.ozon.ru/search/?deny_category_prediction=true&from_global=true&text={text_processing}')
        time.sleep(3)

        try:
            find_links = driver.find_elements(By.CSS_SELECTOR, 'div.tile-root a.tile-clickable-element')
            product_urls = {link.get_attribute("href") for link in find_links if link.get_attribute("href") is not None}

        except Exception as e:
            print(f'[!] Что-то пошло не так при сборе ссылок на товары Ozon: {e}')
            return

        product_urls = list(product_urls)

        print(f'Найдено: {len(product_urls)} товаров')

        count = 0
        for product_url in product_urls:
            if not product_url: continue

            try:
                driver.get(product_url)
                time.sleep(3)

                print('-------')
                print(f'Обработка: {count + 1}/{len(product_urls)}')
                print('-------')

                # Отправляем статус
                requests.post(
                    'http://nodejs-api:3000/api/status',
                    json={
                        'ip': user_ip,
                        'message': f'Ozon: Обработка {count + 1}/{len(product_urls)}'
                    }
                )

                get_products_data_Ozon(product_url, driver=driver, user_ip=user_ip)
                count += 1

            except Exception as e:
                print(f"Ошибка обработки {product_url}: {str(e)}")
                print('-----------------------------')

        print('----')
        print('Данные о товарах упакованы в json')

        print('Отправка json результата на REST_API')
        try:
            with open(f"json products data/{user_ip}-Ozon.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                response = requests.post(
                    'http://nodejs-api:3000/api/data',
                    json={
                        'ip': user_ip,
                        'marketplace': 'Ozon',
                        'data': data
                    }
                )
                print(f"Ответ от API: {response.status_code}")
        except Exception as e:
            print(f"Ошибка при отправке данных в API: {e}")

        # удаление json-файла на сервере
        file_path = f"json products data/{user_ip}-Ozon.json"
        try:
            os.remove(file_path)
            print(f"Файл '{file_path}' успешно удален.")
        except FileNotFoundError:
            print(f"Файл '{file_path}' не найден.")
        except PermissionError:
            print(f"У вас нет прав для удаления файла '{file_path}'.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

    finally:
        driver.quit()
        print("Ozon. Обработка завершена!")
        print('-----------------------------')


def get_products_links_WB(item_name, user_ip):
    driver = uc.Chrome(version_main=135)
    driver.implicitly_wait(10)

    try:
        text_processing = item_name.replace(' ', '%20')
        driver.get(f'https://www.wildberries.ru/catalog/0/search.aspx?search={text_processing}')
        time.sleep(3)

        try:
            find_links = driver.find_elements(By.CSS_SELECTOR, 'a.product-card__link')
            product_urls = {link.get_attribute("href") for link in find_links if link.get_attribute("href") is not None}

        except Exception as e:
            print(f'[!] Что-то пошло не так при сборе ссылок на товары WB: {e}')
            return

        product_urls = list(product_urls)

        print(f'Найдено: {len(product_urls)} товаров')

        count = 0
        for product_url in product_urls:
            if not product_url: continue

            try:
                driver.get(product_url)
                time.sleep(3)

                print('-------')
                print(f'Обработка: {count + 1}/{len(product_urls)}')
                print('-------')

                # Отправляем статус
                requests.post(
                    'http://nodejs-api:3000/api/status',
                    json={
                        'ip': user_ip,
                        'message': f'Ozon: Обработка {count + 1}/{len(product_urls)}'
                    }
                )

                get_products_data_WB(product_url, driver=driver, user_id=user_ip)
                count += 1
            except Exception as e:
                print(f"Ошибка обработки {product_url}: {str(e)}")
                print('-----------------------------')

        print('----')
        print('Данные о товарах упакованы в json')

        print('Отправка json результата на REST_API')
        try:
            with open(f"json products data/{user_ip}-WB.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                response = requests.post(
                    'http://nodejs-api:3000/api/data',
                    json={
                        'ip': user_ip,
                        'marketplace': 'Ozon',
                        'data': data
                    }
                )
                print(f"Ответ от API: {response.status_code}")
        except Exception as e:
            print(f"Ошибка при отправке данных в API: {e}")

        # удаление json-файла на сервере
        file_path = f"json products data/{user_ip}-WB.json"
        try:
            os.remove(file_path)
            print(f"Файл '{file_path}' успешно удален.")
        except FileNotFoundError:
            print(f"Файл '{file_path}' не найден.")
        except PermissionError:
            print(f"У вас нет прав для удаления файла '{file_path}'.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

    finally:
        driver.quit()
        print("Ozon. Обработка завершена!")
        print('-----------------------------')


def get_products_links_YandexMarket(item_name, user_ip):
    driver = uc.Chrome(version_main=135)
    driver.implicitly_wait(15)

    try:
        text_processing = item_name.replace(' ', '%20')
        driver.get(f'https://market.yandex.ru/search?text={text_processing}')
        time.sleep(random.randint(4, 10))

        try:
            find_links = driver.find_elements(By.CSS_SELECTOR, 'a.EQlfk')
            time.sleep(random.randint(5, 10))

            product_urls = {
                link.get_attribute("href") for link in find_links
                if link.get_attribute("href") is not None and "/product--" in link.get_attribute("href")
            }

        except Exception as e:
            print(f'[!] Что-то пошло не так при сборе ссылок на товары Я.Маркет: {e}')

        product_urls = list(product_urls)

        print(f'Найдено: {len(product_urls)} товаров')

        count = 0
        for product_url in product_urls:
            if not product_url: continue

            try:
                driver.get(product_url)
                time.sleep(3)

                print('-------')
                print(f'Обработка: {count + 1}/{len(product_urls)}')
                print('-------')

                # Отправляем статус
                requests.post(
                    'http://nodejs-api:3000/api/status',
                    json={
                        'ip': user_ip,
                        'message': f'Ozon: Обработка {count + 1}/{len(product_urls)}'
                    }
                )

                get_products_data_YandexMarket(product_url, driver=driver, user_id=user_ip)
                count += 1
            except Exception as e:
                print(f'Ошибка обработки {product_url}: {str(e)}')
                print('-----------------------------')

        print('----')
        print('Данные о товарах упакованы в json')

        print('Отправка json результата на REST_API')
        try:
            with open(f"json products data/{user_ip}-YandexMarket.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                response = requests.post(
                    'http://nodejs-api:3000/api/data',
                    json={
                        'ip': user_ip,
                        'marketplace': 'Ozon',
                        'data': data
                    }
                )
                print(f"Ответ от API: {response.status_code}")
        except Exception as e:
            print(f"Ошибка при отправке данных в API: {e}")

        # удаление json-файла на сервере
        file_path = f"json products data/{user_ip}-YandexMarket.json"
        try:
            os.remove(file_path)
            print(f"Файл '{file_path}' успешно удален.")
        except FileNotFoundError:
            print(f"Файл '{file_path}' не найден.")
        except PermissionError:
            print(f"У вас нет прав для удаления файла '{file_path}'.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

    finally:
        driver.quit()
        print("Ozon. Обработка завершена!")
        print('-----------------------------')


def get_products_links_MagnitMarket(item_name, user_ip):
    driver = uc.Chrome(version_main=135)
    driver.implicitly_wait(10)

    try:
        text_processing = item_name.replace(' ', '%20')
        driver.get(f'https://mm.ru/search?query={text_processing}')
        time.sleep(3)

        try:
            find_links = driver.find_elements(By.CSS_SELECTOR, 'div[data-test-id="item__product-card"] a[ui-link="ui-link"]')
            product_urls = {link.get_attribute("href") for link in find_links if link.get_attribute("href") is not None}

        except Exception as e:
            print(f'[!] Что-то пошло не так при сборе ссылок на товары М.Маркет: {e}')

        product_urls = list(product_urls)

        print(f'Найдено: {len(product_urls)} товаров')

        count = 0
        for product_url in product_urls:
            if not product_url: continue

            try:
                driver.get(product_url)
                time.sleep(3)

                print('-------')
                print(f'Обработка: {count+1}/{len(product_urls)}')
                print('-------')

                # Отправляем статус
                requests.post(
                    'http://nodejs-api:3000/api/status',
                    json={
                        'ip': user_ip,
                        'message': f'Ozon: Обработка {count + 1}/{len(product_urls)}'
                    }
                )

                get_products_data_MagnitMarket(product_url, driver=driver, user_id=user_ip)
                count += 1
            except Exception as e:
                print(f'Ошибка обработки {product_url}: {str(e)}')
                print('-----------------------------')

        print('----')
        print('Данные о товарах упакованы в json')

        print('Отправка json результата на REST_API')
        try:
            with open(f"json products data/{user_ip}-MagnitMarket.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                response = requests.post(
                    'http://nodejs-api:3000/api/data',
                    json={
                        'ip': user_ip,
                        'marketplace': 'Ozon',
                        'data': data
                    }
                )
                print(f"Ответ от API: {response.status_code}")
        except Exception as e:
            print(f"Ошибка при отправке данных в API: {e}")


        # удаление json-файла на сервере
        file_path = f"json products data/{user_ip}-MagnitMarket.json"
        try:
            os.remove(file_path)
            print(f"Файл '{file_path}' успешно удален.")
        except FileNotFoundError:
            print(f"Файл '{file_path}' не найден.")
        except PermissionError:
            print(f"У вас нет прав для удаления файла '{file_path}'.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

    finally:
        driver.quit()
        print("Ozon. Обработка завершена!")
        print('-----------------------------')


def get_products_links_DNS(item_name, user_ip):
    driver = uc.Chrome(version_main=135)
    wait = WebDriverWait(driver, 10)

    try:
        driver.get('https://www.dns-shop.ru')
        time.sleep(3)

        find_input = driver.find_element(By.NAME, 'q')
        find_input.clear()
        find_input.send_keys(item_name)
        time.sleep(2)
        find_input.send_keys(Keys.ENTER)
        time.sleep(2)

        try:
            find_links = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.catalog-product__name'))
            )
            product_urls = [link.get_attribute("href") for link in find_links if link.get_attribute("href") is not None]

        except Exception as e:
            print(f'[!] Что-то пошло не так при сборе ссылок на товары DNS: {e}')

        product_urls = list(product_urls)

        count = 0
        for product_url in product_urls:
            if not product_url: continue

            try:
                driver.get(product_url)
                time.sleep(3)

                print('-------')
                print(f'Обработка: {count + 1}/{len(product_urls)}')
                print('-------')

                # Отправляем статус
                requests.post(
                    'http://nodejs-api:3000/api/status',
                    json={
                        'ip': user_ip,
                        'message': f'Ozon: Обработка {count + 1}/{len(product_urls)}'
                    }
                )

                get_products_data_DNS(product_url, driver=driver, user_id=user_ip)
                count += 1
            except Exception as e:
                print(f'Ошибка обработки {product_url}: {str(e)}')
                print('-----------------------------')

        print('----')
        print('Данные о товарах упакованы в json')

        print('Отправка json результата на REST_API')
        try:
            with open(f"json products data/{user_ip}-DNS.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                response = requests.post(
                    'http://nodejs-api:3000/api/data',
                    json={
                        'ip': user_ip,
                        'marketplace': 'Ozon',
                        'data': data
                    }
                )
                print(f"Ответ от API: {response.status_code}")
        except Exception as e:
            print(f"Ошибка при отправке данных в API: {e}")

        # удаление json-файла на сервере
        file_path = f"json products data/{user_ip}-DNS.json"
        try:
            os.remove(file_path)
            print(f"Файл '{file_path}' успешно удален.")
        except FileNotFoundError:
            print(f"Файл '{file_path}' не найден.")
        except PermissionError:
            print(f"У вас нет прав для удаления файла '{file_path}'.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")


    finally:
        driver.quit()
        print("Ozon. Обработка завершена!")
        print('-----------------------------')


def get_products_links_Citilink(item_name, user_ip): # Дописать парсинг картинок
    driver = uc.Chrome(version_main=135)
    driver.implicitly_wait(10)

    try:
        text_processing = item_name.replace(' ', '+')
        driver.get(f'https://www.citilink.ru/search/?text={text_processing}')
        time.sleep(3)

        try:
            find_links = driver.find_elements(By.CSS_SELECTOR, 'a.app-catalog-51bw0j-Anchor--Anchor-Anchor--StyledAnchor')
            product_urls = [link.get_attribute("href") for link in find_links if link.get_attribute("href") is not None]

        except Exception as e:
            print(f'[!] Что-то пошло не так при сборе ссылок на товары Citilink: {e}')

        product_urls = list(product_urls)

        count = 0
        for product_url in product_urls:
            if not product_url: continue

            try:
                driver.get(product_url)
                time.sleep(3)

                print('-------')
                print(f'Обработка: {count + 1}/{len(product_urls)}')
                print('-------')

                # Отправляем статус
                requests.post(
                    'http://nodejs-api:3000/api/status',
                    json={
                        'ip': user_ip,
                        'message': f'Ozon: Обработка {count + 1}/{len(product_urls)}'
                    }
                )

                get_products_data_Citilink(product_url, driver=driver, user_id=user_ip)
                count += 1
            except Exception as e:
                print(f'Ошибка обработки {product_url}: {str(e)}')
                print('-----------------------------')

        print('----')
        print('Данные о товарах упакованы в json')

        print('Отправка json результата на REST_API')
        try:
            with open(f"json products data/{user_ip}-Citilink.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                response = requests.post(
                    'http://nodejs-api:3000/api/data',
                    json={
                        'ip': user_ip,
                        'marketplace': 'Ozon',
                        'data': data
                    }
                )
                print(f"Ответ от API: {response.status_code}")
        except Exception as e:
            print(f"Ошибка при отправке данных в API: {e}")

        # удаление json-файла на сервере
        file_path = f"json products data/{user_ip}-Citilink.json"
        try:
            os.remove(file_path)
            print(f"Файл '{file_path}' успешно удален.")
        except FileNotFoundError:
            print(f"Файл '{file_path}' не найден.")
        except PermissionError:
            print(f"У вас нет прав для удаления файла '{file_path}'.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

    finally:
        driver.quit()
        print("Ozon. Обработка завершена!")
        print('-----------------------------')


def get_products_links_M_Video(item_name, user_ip): # Доработать (Пропадают цены время от времени)
    driver = uc.Chrome(version_main=135)
    driver.implicitly_wait(10)

    try:
        text_processing = item_name.replace(' ', '+')
        driver.get(f'https://www.mvideo.ru/product-list-page?q={text_processing}')
        time.sleep(3)

        try:
            find_links = driver.find_elements(By.CSS_SELECTOR, 'a.product-title__text')
            product_urls = [link.get_attribute("href") for link in find_links if link.get_attribute("href") is not None]

        except Exception as e:
            print(f'[!] Что-то пошло не так при сборе ссылок на товары M.Video: {e}')

        product_urls = list(product_urls)

        count = 0
        for product_url in product_urls:
            if not product_url: continue

            try:
                driver.get(product_url)
                time.sleep(3)

                print('-------')
                print(f'Обработка: {count + 1}/{len(product_urls)}')
                print('-------')

                # Отправляем статус
                requests.post(
                    'http://nodejs-api:3000/api/status',
                    json={
                        'ip': user_ip,
                        'message': f'Ozon: Обработка {count + 1}/{len(product_urls)}'
                    }
                )

                get_products_data_M_Video(product_url, driver=driver, user_id=user_ip)
                count += 1
            except Exception as e:
                print(f'Ошибка обработки {product_url}: {str(e)}')
                print('-----------------------------')

        print('----')
        print('Данные о товарах упакованы в json')

        print('Отправка json результата на REST_API')
        try:
            with open(f"json products data/{user_ip}-M_Video.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                response = requests.post(
                    'http://nodejs-api:3000/api/data',
                    json={
                        'ip': user_ip,
                        'marketplace': 'Ozon',
                        'data': data
                    }
                )
                print(f"Ответ от API: {response.status_code}")
        except Exception as e:
            print(f"Ошибка при отправке данных в API: {e}")

        # удаление json-файла на сервере
        file_path = f"json products data/{user_ip}-M_Video.json"
        try:
            os.remove(file_path)
            print(f"Файл '{file_path}' успешно удален.")
        except FileNotFoundError:
            print(f"Файл '{file_path}' не найден.")
        except PermissionError:
            print(f"У вас нет прав для удаления файла '{file_path}'.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

    finally:
        driver.quit()
        print("Ozon. Обработка завершена!")
        print('-----------------------------')


# def get_products_links_Avito(item_name, user_id):
#     driver = uc.Chrome(version_main=135)
#     driver.implicitly_wait(10)
#
#     try:
#         driver.get('https://www.avito.ru')
#         time.sleep(3)
#
#         find_input = driver.find_element(By.ID, 'bx_search')
#         find_input.clear()
#         for char in item_name:
#             find_input.send_keys(char)
#             time.sleep(0.1)
#         time.sleep(2)
#         find_input.send_keys(Keys.ENTER)
#         time.sleep(2)
#
#         try:
#             find_links = driver.find_elements(By.CSS_SELECTOR, 'a[itemprop="url"]')
#             #product_urls = [link.get_attribute("href") for link in find_links if link.get_attribute("href") is not None]
#             product_urls = {link.get_attribute("href") for link in find_links if link.get_attribute("href") is not None}
#
#         except Exception as e:
#             print(f'[!] Что-то пошло не так при сборе ссылок на товары Avito: {e}')
#
#         product_urls = list(product_urls)
#
#         count = 0
#         for product_url in product_urls:
#             if not product_url: continue
#
#             try:
#                 driver.get(product_url)
#                 time.sleep(3)
#
#                 print('-------')
#                 print(f'Обработка: {count + 1}/{len(product_urls)}')
#                 print('-------')
#
#                 get_products_data_Avito(product_url, driver=driver, user_id=user_id)
#                 count += 1
#             except Exception as e:
#                 print(f'Ошибка обработки {product_url}: {str(e)}')
#                 print('-----------------------------')
#
#         print('----')
#         print('Данные о товарах упакованы в json')
#         # отправка json результата на REST_API
#
#         # удаление json-файла на сервере
#         # file_path = f"json products data/{user_id}-M_Video.json"
#         # try:
#         #     os.remove(file_path)
#         #     print(f"Файл '{file_path}' успешно удален.")
#         # except FileNotFoundError:
#         #     print(f"Файл '{file_path}' не найден.")
#         # except PermissionError:
#         #     print(f"У вас нет прав для удаления файла '{file_path}'.")
#         # except Exception as e:
#         #     print(f"Произошла ошибка: {e}")
#
#     finally:
#         driver.quit()
#         print("Ozon. Обработка завершена!")
#         print('-----------------------------')
#
#
# def get_products_links_Youla(item_name, user_id):
#     driver = uc.Chrome(version_main=135)
#     driver.implicitly_wait(10)
#
#     try:
#         driver.get('https://www.youla.ru')
#         time.sleep(3)
#
#         find_input = driver.find_element(By.ID, 'downshift-0-input')
#         find_input.clear()
#         find_input.send_keys(item_name)
#         time.sleep(2)
#         find_input.send_keys(Keys.ENTER)
#         time.sleep(2)
#
#
#         try:
#             find_links = driver.find_elements(By.CSS_SELECTOR, 'a[target="_blank"][rel="noopener noreferrer"]')
#             product_urls = {
#                 link.get_attribute("href") for link in find_links
#                 if link.get_attribute("href") is not None and "source_view=search" in link.get_attribute("href")
#             }
#
#         except Exception as e:
#             print(f'[!] Что-то пошло не так при сборе ссылок на товары Youla: {e}')
#
#         product_urls = list(product_urls)
#
#         count = 0
#         for product_url in product_urls:
#             if not product_url: continue
#
#             try:
#                 driver.get(product_url)
#                 time.sleep(3)
#
#                 print('-------')
#                 print(f'Обработка: {count + 1}/{len(product_urls)}')
#                 print('-------')
#
#                 get_products_data_Youla(product_url, driver=driver, user_id=user_id)
#                 count += 1
#             except Exception as e:
#                 print(f'Ошибка обработки {product_url}: {str(e)}')
#                 print('-----------------------------')
#
#         print('----')
#         print('Данные о товарах упакованы в json')
#         # отправка json результата на REST_API
#
#         # удаление json-файла на сервере
#         # file_path = f"json products data/{user_id}-M_Video.json"
#         # try:
#         #     os.remove(file_path)
#         #     print(f"Файл '{file_path}' успешно удален.")
#         # except FileNotFoundError:
#         #     print(f"Файл '{file_path}' не найден.")
#         # except PermissionError:
#         #     print(f"У вас нет прав для удаления файла '{file_path}'.")
#         # except Exception as e:
#         #     print(f"Произошла ошибка: {e}")
#
#     finally:
#         driver.quit()
#         print("Ozon. Обработка завершена!")
#         print('-----------------------------')


def get_products_links_Aliexpress(item_name, user_ip):
    driver = uc.Chrome(version_main=135)
    driver.implicitly_wait(10)

    try:
        text_processing = item_name.replace(' ', '+')
        driver.get(f'https://aliexpress.ru/wholesale?SearchText={text_processing}')
        time.sleep(3)

        try:
            find_links = driver.find_elements(By.CSS_SELECTOR, 'a.red-snippet_RedSnippet__gallery__e15tmk')
            product_urls = [link.get_attribute("href") for link in find_links if link.get_attribute("href") is not None]

        except Exception as e:
            print(f'[!] Что-то пошло не так при сборе ссылок на товары Aliexpress: {e}')

        product_urls = list(product_urls)

        count = 0
        for product_url in product_urls:
            if not product_url: continue

            try:
                driver.get(product_url)
                time.sleep(3)

                print('-------')
                print(f'Обработка: {count + 1}/{len(product_urls)}')
                print('-------')

                # Отправляем статус
                requests.post(
                    'http://nodejs-api:3000/api/status',
                    json={
                        'ip': user_ip,
                        'message': f'Ozon: Обработка {count + 1}/{len(product_urls)}'
                    }
                )

                get_products_data_Aliexpress(product_url, driver=driver, user_id=user_ip)
                count += 1
            except Exception as e:
                print(f'Ошибка обработки {product_url}: {str(e)}')
                print('-----------------------------')

        print('----')
        print('Данные о товарах упакованы в json')

        print('Отправка json результата на REST_API')
        try:
            with open(f"json products data/{user_ip}-Aliexpress.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                response = requests.post(
                    'http://nodejs-api:3000/api/data',
                    json={
                        'ip': user_ip,
                        'marketplace': 'Ozon',
                        'data': data
                    }
                )
                print(f"Ответ от API: {response.status_code}")
        except Exception as e:
            print(f"Ошибка при отправке данных в API: {e}")

        # удаление json-файла на сервере
        file_path = f"json products data/{user_ip}-Aliexpress.json"
        try:
            os.remove(file_path)
            print(f"Файл '{file_path}' успешно удален.")
        except FileNotFoundError:
            print(f"Файл '{file_path}' не найден.")
        except PermissionError:
            print(f"У вас нет прав для удаления файла '{file_path}'.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")


    finally:
        driver.quit()
        print("Ozon. Обработка завершена!")
        print('-----------------------------')


def get_products_links_Joom(item_name, user_ip):
    driver = uc.Chrome(version_main=135)
    driver.implicitly_wait(10)

    try:
        text_processing = item_name.replace(' ', '+')
        driver.get(f'https://www.joom.ru/ru/search/q.{text_processing}')
        time.sleep(3)

        try:
            find_links = driver.find_elements(By.CSS_SELECTOR, 'a.content___N4xbX')
            product_urls = [link.get_attribute("href") for link in find_links if link.get_attribute("href") is not None]

        except Exception as e:
            print(f'[!] Что-то пошло не так при сборе ссылок на товары Joom: {e}')

        product_urls = list(product_urls)

        count = 0
        for product_url in product_urls:
            if not product_url: continue

            try:
                driver.get(product_url)
                time.sleep(3)

                print('-------')
                print(f'Обработка: {count + 1}/{len(product_urls)}')
                print('-------')

                # Отправляем статус
                requests.post(
                    'http://nodejs-api:3000/api/status',
                    json={
                        'ip': user_ip,
                        'message': f'Ozon: Обработка {count + 1}/{len(product_urls)}'
                    }
                )

                get_products_data_Joom(product_url, driver=driver, user_id=user_ip)
                count += 1
            except Exception as e:
                print(f'Ошибка обработки {product_url}: {str(e)}')
                print('-----------------------------')

        print('----')
        print('Данные о товарах упакованы в json')

        print('Отправка json результата на REST_API')
        try:
            with open(f"json products data/{user_ip}-Joom.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                response = requests.post(
                    'http://nodejs-api:3000/api/data',
                    json={
                        'ip': user_ip,
                        'marketplace': 'Ozon',
                        'data': data
                    }
                )
                print(f"Ответ от API: {response.status_code}")
        except Exception as e:
            print(f"Ошибка при отправке данных в API: {e}")


        # удаление json-файла на сервере
        file_path = f"json products data/{user_ip}-Joom.json"
        try:
            os.remove(file_path)
            print(f"Файл '{file_path}' успешно удален.")
        except FileNotFoundError:
            print(f"Файл '{file_path}' не найден.")
        except PermissionError:
            print(f"У вас нет прав для удаления файла '{file_path}'.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")


    finally:
        driver.quit()
        print("Ozon. Обработка завершена!")
        print('-----------------------------')


def get_products_links_Shop_mts(item_name, user_ip):
    driver = uc.Chrome(version_main=135)
    driver.implicitly_wait(10)

    try:
        text_processing = item_name.replace(' ', '%20')
        driver.get(f'https://shop.mts.ru/search/?TYPE=products&q={text_processing}')
        time.sleep(3)

        try:
            find_links = driver.find_elements(By.CSS_SELECTOR, 'a.product-card__gallery-wrap')
            product_urls = {link.get_attribute("href") for link in find_links if link.get_attribute("href") is not None}

        except Exception as e:
            print(f'[!] Что-то пошло не так при сборе ссылок на товары Shop.mts: {e}')

        product_urls = list(product_urls)

        count = 0
        for product_url in product_urls:
            if not product_url: continue

            try:
                driver.get(product_url)
                time.sleep(3)

                print('-------')
                print(f'Обработка: {count + 1}/{len(product_urls)}')
                print('-------')

                # Отправляем статус
                requests.post(
                    'http://nodejs-api:3000/api/status',
                    json={
                        'ip': user_ip,
                        'message': f'Ozon: Обработка {count + 1}/{len(product_urls)}'
                    }
                )

                get_products_data_Shop_mts(product_url, driver=driver, user_id=user_ip)
                count += 1
            except Exception as e:
                print(f'Ошибка обработки {product_url}: {str(e)}')
                print('-----------------------------')

        print('----')
        print('Данные о товарах упакованы в json')

        print('Отправка json результата на REST_API')
        try:
            with open(f"json products data/{user_ip}-Shop_mts.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                response = requests.post(
                    'http://nodejs-api:3000/api/data',
                    json={
                        'ip': user_ip,
                        'marketplace': 'Ozon',
                        'data': data
                    }
                )
                print(f"Ответ от API: {response.status_code}")
        except Exception as e:
            print(f"Ошибка при отправке данных в API: {e}")

        # удаление json-файла на сервере
        file_path = f"json products data/{user_ip}-Shop_mts.json"
        try:
            os.remove(file_path)
            print(f"Файл '{file_path}' успешно удален.")
        except FileNotFoundError:
            print(f"Файл '{file_path}' не найден.")
        except PermissionError:
            print(f"У вас нет прав для удаления файла '{file_path}'.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")


    finally:
        driver.quit()
        print("Ozon. Обработка завершена!")
        print('-----------------------------')


def get_products_links_Technopark(item_name, user_ip):
    driver = uc.Chrome(version_main=135)
    driver.implicitly_wait(10)

    try:
        text_processing = item_name.replace(' ', '%20')
        driver.get(f'https://www.technopark.ru/search/?q={text_processing}')
        time.sleep(3)

        try:
            find_links = driver.find_elements(By.CSS_SELECTOR, 'a.product-card-link.product-card-big__image-wrapper')
            product_urls = {link.get_attribute("href") for link in find_links if link.get_attribute("href") is not None}

        except Exception as e:
            print(f'[!] Что-то пошло не так при сборе ссылок на товары Technopark: {e}')

        product_urls = list(product_urls)

        count = 0
        for product_url in product_urls:
            if not product_url: continue

            try:
                driver.get(product_url)
                time.sleep(3)

                print('-------')
                print(f'Обработка: {count + 1}/{len(product_urls)}')
                print('-------')

                # Отправляем статус
                requests.post(
                    'http://nodejs-api:3000/api/status',
                    json={
                        'ip': user_ip,
                        'message': f'Ozon: Обработка {count + 1}/{len(product_urls)}'
                    }
                )

                get_products_data_Technopark(product_url, driver=driver, user_id=user_ip)
                count += 1
            except Exception as e:
                print(f'Ошибка обработки {product_url}: {str(e)}')
                print('-----------------------------')

        print('----')
        print('Данные о товарах упакованы в json')

        print('Отправка json результата на REST_API')
        try:
            with open(f"json products data/{user_ip}-Technopark.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                response = requests.post(
                    'http://nodejs-api:3000/api/data',
                    json={
                        'ip': user_ip,
                        'marketplace': 'Ozon',
                        'data': data
                    }
                )
                print(f"Ответ от API: {response.status_code}")
        except Exception as e:
            print(f"Ошибка при отправке данных в API: {e}")

        # удаление json-файла на сервере
        file_path = f"json products data/{user_ip}-Technopark.json"
        try:
            os.remove(file_path)
            print(f"Файл '{file_path}' успешно удален.")
        except FileNotFoundError:
            print(f"Файл '{file_path}' не найден.")
        except PermissionError:
            print(f"У вас нет прав для удаления файла '{file_path}'.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")


    finally:
        driver.quit()
        print("Ozon. Обработка завершена!")
        print('-----------------------------')


def get_products_links_Lamoda(item_name, user_ip):
    driver = uc.Chrome(version_main=135)
    driver.implicitly_wait(10)

    try:
        text_processing = item_name.replace(' ', '%20')
        driver.get(f'https://www.lamoda.ru/catalogsearch/result/?q={text_processing}')
        time.sleep(3)

        try:
            find_links = driver.find_elements(By.CSS_SELECTOR, 'a._root_aroml_2.x-product-card__pic')
            product_urls = {link.get_attribute("href") for link in find_links if link.get_attribute("href") is not None}

        except Exception as e:
            print(f'[!] Что-то пошло не так при сборе ссылок на товары Lamoda: {e}')

        product_urls = list(product_urls)

        count = 0
        for product_url in product_urls:
            if not product_url: continue

            try:
                driver.get(product_url)
                time.sleep(3)

                print('-------')
                print(f'Обработка: {count + 1}/{len(product_urls)}')
                print('-------')

                # Отправляем статус
                requests.post(
                    'http://nodejs-api:3000/api/status',
                    json={
                        'ip': user_ip,
                        'message': f'Ozon: Обработка {count + 1}/{len(product_urls)}'
                    }
                )

                get_products_data_Lamoda(product_url, driver=driver, user_id=user_ip)
                count += 1
            except Exception as e:
                print(f'Ошибка обработки {product_url}: {str(e)}')
                print('-----------------------------')

        print('----')
        print('Данные о товарах упакованы в json')

        print('Отправка json результата на REST_API')
        try:
            with open(f"json products data/{user_ip}-Lamoda.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                response = requests.post(
                    'http://nodejs-api:3000/api/data',
                    json={
                        'ip': user_ip,
                        'marketplace': 'Ozon',
                        'data': data
                    }
                )
                print(f"Ответ от API: {response.status_code}")
        except Exception as e:
            print(f"Ошибка при отправке данных в API: {e}")

        # удаление json-файла на сервере
        file_path = f"json products data/{user_ip}-Lamoda.json"
        try:
            os.remove(file_path)
            print(f"Файл '{file_path}' успешно удален.")
        except FileNotFoundError:
            print(f"Файл '{file_path}' не найден.")
        except PermissionError:
            print(f"У вас нет прав для удаления файла '{file_path}'.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")


    finally:
        driver.quit()
        print("Ozon. Обработка завершена!")
        print('-----------------------------')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

# def main():
#     get_products_links_html_Ozon('наушники xiaomi', user_id='12331224') # 16.86 time.sleep(7) | 13.01 time.sleep(3) | 7.40 query optimization
#     get_products_links_WB('наушники xiaomi', user_id='12331224') # 14.31 time.sleep(5) | 13.10 time.sleep(3) | 9.13 query optimization
#     get_products_links_YandexMarket('наушники xiaomi', user_id='12331224') # 19.83 time.sleep(4) | 18.38 time.sleep(3) | 13.15 query optimization
#     get_products_links_MagnitMarket('наушники xiaomi', user_id='12331224')  #35.72 time.sleep(3) | 18.47 time.sleep(3) | 30.49 query optimization
#     get_products_links_DNS('наушники xiaomi', user_id='12331224') # 42.17 time.sleep(3) | 53.38 time.sleep(3)
#     get_products_links_Citilink('наушники xiaomi', user_id='12331224') # 19.88 time.sleep(3) | 16.72 time.sleep(3) | 9.55 query optimization
#     get_products_links_M_Video('наушники xiaomi', user_id='12331224') # 14.69 time.sleep(3) | 14.53 time.sleep(3) | 9.62 query optimization
#     #get_products_links_Avito('наушники xiaomi', user_id='12331224') # 95.88 time.sleep(3) | 96.14 time.sleep(3)
#     #get_products_links_Youla('наушники xiaomi', user_id='12331224') # 20.92 time.sleep(3) | 17.54 time.sleep(3)
#     get_products_links_Aliexpress('наушники xiaomi', user_id='12331224') # 23.63 time.sleep(7) | 19.37 time.sleep(3) | 19.95 query optimization
#     get_products_links_Joom('наушники xiaomi', user_id='12331224') # 18.28 time.sleep(7) | 15.63 time.sleep(3) | 9.49 query optimization
#     get_products_links_Shop_mts('наушники xiaomi', user_id='12331224') # 30.15 time.sleep(7) | 28.37 time.sleep(3) | 12.60 query optimization
#     get_products_links_Technopark('наушники xiaomi', user_id='12331224') # 40.60 time.sleep(7) | 38.19 time.sleep(3) | 31.43 query optimization
#     get_products_links_Lamoda('кроссовки nike', user_id='12331224') # 21.49 time.sleep(7) | 16.93 time.sleep(3) | 32.77 query optimization
#
#
# if __name__ == '__main__':
#     main()
