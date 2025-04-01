import json
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_products_data_Ozon(link_products, driver):
    print(f'Ссылка на товар:{link_products}')

    WebDriverWait(driver, 10).until(
        EC.any_of(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.ga122-a2.tsBodyControl400Small")),
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1.lz7_28.tsHeadline550Medium")),
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.ga122-a2.tsBodyControl500Medium")),
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.zl0_28.z0l_28.zl4_28"))
        )
    )

    article_number = driver.find_elements(By.CSS_SELECTOR, "div.ga122-a2.tsBodyControl400Small")
    name_products = driver.find_elements(By.CSS_SELECTOR, "h1.lz7_28.tsHeadline550Medium")
    rating = driver.find_elements(By.CSS_SELECTOR, "div.ga122-a2.tsBodyControl500Medium")
    price = driver.find_elements(By.CSS_SELECTOR, "span.zl0_28.z0l_28.zl4_28")


    def review_processing(number_of_reviews):
        number_of_reviews = number_of_reviews.replace(' отзывов', '').replace(' отзыва', '')
        cleaned_reviews = number_of_reviews.replace(" ", "")
        if cleaned_reviews.isdigit():
            print(f'Количество отзывов:{number_of_reviews}')
        else:
            print(
                f'Не удалось отформатировать кол-во отзывов. Исходные данные:{number_of_reviews}, {cleaned_reviews}')


    if not article_number:
        print(f"Элемент 'article_number' не найден")
    else:
        print(article_number[2].text)


    if not name_products:
        print("Элемент 'name_products' не найден")
    else:
        print(f'Название товара: {name_products[0].text}')

    if not rating:
        print("Элемент 'rating' не найден")
    else:
        if "." in rating[0].text:
            product_rating = rating[0].text[:3]
            number_of_reviews = rating[0].text[5:]
            print(f'Рейтинг товара: {product_rating}')
            review_processing(number_of_reviews)
        else:
            product_rating = rating[0].text[:1]
            print(f'Рейтинг товара: {product_rating}')
            number_of_reviews = rating[0].text[3:]
            review_processing(number_of_reviews)

    if not price:
        print("Элемент 'price' не найден")
    else:
        product_price = price[0].text[:-2]
        print(f'Цена товара: {product_price}')


    # Картинки
    try:
        img_element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (By.XPATH, "//img[contains(@src, '/wc1000/')]")
            )
        )

        WebDriverWait(driver, 5).until(EC.visibility_of(img_element))

        image_url = img_element.get_attribute('src') or img_element.get_attribute('data-src')
        print(f"Найдено изображение: {image_url}")

    except Exception as e:
        print(f"Ошибка: {str(e)}")

    print('-------------')
