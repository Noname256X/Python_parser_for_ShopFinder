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



def get_products_links_html_Ozon(item_name, user_id):
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

                get_products_data_Ozon(product_url, driver=driver, user_id=user_id)
                count += 1

            except Exception as e:
                print(f"Ошибка обработки {product_url}: {str(e)}")
                print('-----------------------------')

        print('Данные о товарах упакованы в json') # доработать
        # отправка json результата на REST_API

        # удаление json-файла на сервере
        file_path = f"json products data/{user_id}-Ozon.json"
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


def get_products_links_WB(item_name, user_id):
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

                get_products_data_WB(product_url, driver=driver, user_id=user_id)
                count += 1
            except Exception as e:
                print(f"Ошибка обработки {product_url}: {str(e)}")
                print('-----------------------------')

        print('Данные о товарах упакованы в json') # доработать
        # отправка json результата на REST_API

        # удаление json-файла на сервере
        file_path = f"json products data/{user_id}-WB.json"
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


def get_products_links_YandexMarket(item_name, user_id):
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

                get_products_data_YandexMarket(product_url, driver=driver, user_id=user_id)
                count += 1
            except Exception as e:
                print(f'Ошибка обработки {product_url}: {str(e)}')
                print('-----------------------------')

        print('Данные о товарах упакованы в json') # доработать
        # отправка json результата на REST_API

        # удаление json-файла на сервере
        file_path = f"json products data/{user_id}-YandexMarket.json"
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


def get_products_links_MagnitMarket(item_name, user_id):
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

                get_products_data_MagnitMarket(product_url, driver=driver, user_id=user_id)
                count += 1
            except Exception as e:
                print(f'Ошибка обработки {product_url}: {str(e)}')
                print('-----------------------------')

        print('Данные о товарах упакованы в json')  # доработать
        # отправка json результата на REST_API


        # удаление json-файла на сервере
        file_path = f"json products data/{user_id}-MagnitMarket.json"
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


def get_products_links_DNS(item_name):
    driver = uc.Chrome(version_main=135)
    driver.implicitly_wait(10)

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
            find_links = driver.find_elements(By.CSS_SELECTOR, 'a.catalog-product__name')
            product_urls = [link.get_attribute("href") for link in find_links if link.get_attribute("href") is not None]

        except Exception as e:
            print(f'[!] Что-то пошло не так при сборе ссылок на товары DNS: {e}')

        product_urls = list(product_urls)

        if product_urls:
            with open('links to json products/products_urls_dns.json', 'w', encoding='utf-8') as file:
                json.dump(product_urls, file, indent=4, ensure_ascii=False)
            print(f'[+] Ссылки на товары DNS сохранены в файл!')
        else:
            print('[!] Не удалось собрать ссылки на товары DNS.')

    finally:
        driver.quit()
        print("Ozon. Обработка завершена!")
        print('-----------------------------')


def get_products_links_Citilink(item_name):
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

        if product_urls:
            with open('links to json products/products_urls_citilink.json', 'w', encoding='utf-8') as file:
                json.dump(product_urls, file, indent=4, ensure_ascii=False)
            print(f'[+] Ссылки на товары Citilink сохранены в файл!')
        else:
            print('[!] Не удалось собрать ссылки на товары Citilink.')

    finally:
        driver.quit()
        print("Ozon. Обработка завершена!")
        print('-----------------------------')


# def Eldorado (captcha)


def get_products_links_M_Video(item_name):
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

        if product_urls:
            with open('links to json products/products_urls_m_video.json', 'w', encoding='utf-8') as file:
                json.dump(product_urls, file, indent=4, ensure_ascii=False)
            print(f'[+] Ссылки на товары M.Video сохранены в файл!')
        else:
            print('[!] Не удалось собрать ссылки на товары M.Video.')

    finally:
        driver.quit()
        print("Ozon. Обработка завершена!")
        print('-----------------------------')


def get_products_links_Avito(item_name):
    driver = uc.Chrome(version_main=135)
    driver.implicitly_wait(10)

    try:
        driver.get('https://www.avito.ru')
        time.sleep(3)

        find_input = driver.find_element(By.ID, 'bx_search')
        find_input.clear()
        for char in item_name:
            find_input.send_keys(char)
            time.sleep(0.1)
        time.sleep(2)
        find_input.send_keys(Keys.ENTER)
        time.sleep(2)

        try:
            find_links = driver.find_elements(By.CSS_SELECTOR, 'a[itemprop="url"]')
            #product_urls = [link.get_attribute("href") for link in find_links if link.get_attribute("href") is not None]
            product_urls = {link.get_attribute("href") for link in find_links if link.get_attribute("href") is not None}

        except Exception as e:
            print(f'[!] Что-то пошло не так при сборе ссылок на товары Avito: {e}')

        product_urls = list(product_urls)

        if product_urls:
            with open('links to json products/products_urls_avito.json', 'w', encoding='utf-8') as file:
                json.dump(product_urls, file, indent=4, ensure_ascii=False)
            print(f'[+] Ссылки на товары Avito сохранены в файл!')
        else:
            print('[!] Не удалось собрать ссылки на товары Avito.')

    finally:
        driver.quit()
        print("Ozon. Обработка завершена!")
        print('-----------------------------')


def get_products_links_Youla(item_name):
    driver = uc.Chrome(version_main=135)
    driver.implicitly_wait(10)

    try:
        driver.get('https://www.youla.ru')
        time.sleep(3)

        find_input = driver.find_element(By.ID, 'downshift-0-input')
        find_input.clear()
        find_input.send_keys(item_name)
        time.sleep(2)
        find_input.send_keys(Keys.ENTER)
        time.sleep(2)


        try:
            find_links = driver.find_elements(By.CSS_SELECTOR, 'a[target="_blank"][rel="noopener noreferrer"]')
            product_urls = {
                link.get_attribute("href") for link in find_links
                if link.get_attribute("href") is not None and "source_view=search" in link.get_attribute("href")
            }

        except Exception as e:
            print(f'[!] Что-то пошло не так при сборе ссылок на товары Youla: {e}')

        product_urls = list(product_urls)

        if product_urls:
            with open('links to json products/products_urls_youla.json', 'w', encoding='utf-8') as file:
                json.dump(product_urls, file, indent=4, ensure_ascii=False)
            print(f'[+] Ссылки на товары Youla сохранены в файл!')
        else:
            print('[!] Не удалось собрать ссылки на товары Youla.')

    finally:
        driver.quit()
        print("Ozon. Обработка завершена!")
        print('-----------------------------')


def get_products_links_Aliexpress(item_name):
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

        if product_urls:
            with open('links to json products/products_urls_aliexpress.json', 'w', encoding='utf-8') as file:
                json.dump(product_urls, file, indent=4, ensure_ascii=False)
            print(f'[+] Ссылки на товары Aliexpress сохранены в файл!')
        else:
            print('[!] Не удалось собрать ссылки на товары Aliexpress.')


    finally:
        driver.quit()
        print("Ozon. Обработка завершена!")
        print('-----------------------------')


def get_products_links_Joom(item_name):
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

        if product_urls:
            with open('links to json products/products_urls_joom.json', 'w', encoding='utf-8') as file:
                json.dump(product_urls, file, indent=4, ensure_ascii=False)
            print(f'[+] Ссылки на товары Joom сохранены в файл!')
        else:
            print('[!] Не удалось собрать ссылки на товары Joom.')


    finally:
        driver.quit()
        print("Ozon. Обработка завершена!")
        print('-----------------------------')


def get_products_links_PochtaMarket(item_name):
    driver = uc.Chrome(version_main=135)
    driver.implicitly_wait(10)

    try:
        driver.get('https://market.pochta.ru')
        #time.sleep(7)

        find_input = driver.find_element(By.NAME, 'query')
        find_input.clear()
        find_input.send_keys(item_name)
        #time.sleep(2)
        find_input.send_keys(Keys.ENTER)
        #time.sleep(2)

        try:
            find_links = driver.find_elements(By.CSS_SELECTOR, 'a[ng-href]')
            product_urls = {
                link.get_attribute("href") for link in find_links
                if link.get_attribute("href") is not None and "/product" in link.get_attribute("href")
            }


        except Exception as e:
            print(f'[!] Что-то пошло не так при сборе ссылок на товары PochtaMarket: {e}')

        product_urls = list(product_urls)

        if product_urls:
            with open('links to json products/products_urls_pochta_market.json', 'w', encoding='utf-8') as file:
                json.dump(product_urls, file, indent=4, ensure_ascii=False)
            print(f'[+] Ссылки на товары PochtaMarket сохранены в файл!')
        else:
            print('[!] Не удалось собрать ссылки на товары PochtaMarket.')


    finally:
        driver.quit()
        print("Ozon. Обработка завершена!")
        print('-----------------------------')


def get_products_links_MegaMarket(item_name):
    driver = uc.Chrome(version_main=135)
    driver.implicitly_wait(10)

    try:
        text_processing = item_name.replace(' ', '%20')
        driver.get(f'https://megamarket.ru/catalog/?q={text_processing}')
        time.sleep(3)

        try:
            find_links = driver.find_elements(By.CSS_SELECTOR, 'a.catalog-item-regular-desktop__title-link')
            product_urls = {link.get_attribute("href") for link in find_links if link.get_attribute("href") is not None}

        except Exception as e:
            print(f'[!] Что-то пошло не так при сборе ссылок на товары MegaMarket: {e}')

        product_urls = list(product_urls)

        if product_urls:
            with open('links to json products/products_urls_mega_market.json', 'w', encoding='utf-8') as file:
                json.dump(product_urls, file, indent=4, ensure_ascii=False)
            print(f'[+] Ссылки на товары MegaMarket сохранены в файл!')
        else:
            print('[!] Не удалось собрать ссылки на товары MegaMarket.')


    finally:
        driver.quit()
        print("Ozon. Обработка завершена!")
        print('-----------------------------')


def get_products_links_Shop_mts(item_name):
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

        if product_urls:
            with open('links to json products/products_urls_shop_mts.json', 'w', encoding='utf-8') as file:
                json.dump(product_urls, file, indent=4, ensure_ascii=False)
            print(f'[+] Ссылки на товары Shop.mts сохранены в файл!')
        else:
            print('[!] Не удалось собрать ссылки на товары Shop.mts.')


    finally:
        driver.quit()
        print("Ozon. Обработка завершена!")
        print('-----------------------------')


def get_products_links_Technopark(item_name):
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

        if product_urls:
            with open('links to json products/products_urls_technopark.json', 'w', encoding='utf-8') as file:
                json.dump(product_urls, file, indent=4, ensure_ascii=False)
            print(f'[+] Ссылки на товары Technopark сохранены в файл!')
        else:
            print('[!] Не удалось собрать ссылки на товары Technopark.')


    finally:
        driver.quit()
        print("Ozon. Обработка завершена!")
        print('-----------------------------')


def get_products_links_Lamoda(item_name):
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

        if product_urls:
            with open('links to json products/products_urls_lamoda.json', 'w', encoding='utf-8') as file:
                json.dump(product_urls, file, indent=4, ensure_ascii=False)
            print(f'[+] Ссылки на товары Lamoda сохранены в файл!')
        else:
            print('[!] Не удалось собрать ссылки на товары Lamoda.')


    finally:
        driver.quit()
        print("Ozon. Обработка завершена!")
        print('-----------------------------')


def main():
    get_products_links_html_Ozon('наушники xiaomi', user_id='12331224') # 16.86 time.sleep(7) | 13.01 time.sleep(3) | 7.40 query optimization
    get_products_links_WB('наушники xiaomi', user_id='12331224') # 14.31 time.sleep(5) | 13.10 time.sleep(3) | 9.13 query optimization
    get_products_links_YandexMarket('наушники xiaomi', user_id='12331224') # 19.83 time.sleep(4) | 18.38 time.sleep(3) | 13.15 query optimization
    get_products_links_MagnitMarket('наушники xiaomi', user_id='12331224')  #35.72 time.sleep(3) | 18.47 time.sleep(3) | 30.49 query optimization
    #get_products_links_DNS('наушники xiaomi') # 42.17 time.sleep(3) | 53.38 time.sleep(3)
    #get_products_links_Citilink('наушники xiaomi') # 19.88 time.sleep(3) | 16.72 time.sleep(3) | 9.55 query optimization
    #get_products_links_M_Video('наушники xiaomi') # 14.69 time.sleep(3) | 14.53 time.sleep(3) | 9.62 query optimization
    #get_products_links_Avito('наушники xiaomi') # 95.88 time.sleep(3) | 96.14 time.sleep(3)
    #get_products_links_Youla('наушники xiaomi') # 20.92 time.sleep(3) | 17.54 time.sleep(3)
    #get_products_links_Aliexpress('наушники xiaomi') # 23.63 time.sleep(7) | 19.37 time.sleep(3) | 19.95 query optimization
    #get_products_links_Joom('наушники xiaomi') # 18.28 time.sleep(7) | 15.63 time.sleep(3) | 9.49 query optimization
    #get_products_links_PochtaMarket('наушники xiaomi') # 9.86 no time.sleep() | 8.82 no time.sleep()
    #get_products_links_MegaMarket('наушники xiaomi') # 56.33 time.sleep(7) | 58.16 time.sleep(3) | 50.78 query optimization
    #get_products_links_Shop_mts('наушники xiaomi') # 30.15 time.sleep(7) | 28.37 time.sleep(3) | 12.60 query optimization
    #get_products_links_Technopark('наушники xiaomi') # 40.60 time.sleep(7) | 38.19 time.sleep(3) | 31.43 query optimization
    #get_products_links_Lamoda('кроссовки nike') # 21.49 time.sleep(7) | 16.93 time.sleep(3) | 32.77 query optimization

    # 1. стандарт 480.6 сек. (8,01 мин) в однопотоке
    # 2. time.sleep(3) 447,04 сек. (7,45 мин) в однопотоке
    # 3. query optimization 412,24 сек. (6,87 мин))


if __name__ == '__main__':
    main()
