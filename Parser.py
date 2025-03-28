import json
import time
import os
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_products_data_Ozon(link_products, htmlpath):
    with open(htmlpath, encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")

    article_number = soup.find_all('div', class_='ga122-a2 tsBodyControl400Small')
    name_products = soup.find('h1', class_='lz6_28 tsHeadline550Medium')
    rating = soup.find('div', class_='ga122-a2 tsBodyControl500Medium')
    price = soup.find('span', class_='lz_28 zl_28 zl3_28')
    description = 'позже добавить описание'
    #print(f'ссылка на продукт: {link_products}')
    #print(f'название файла, который парсится: {htmlpath}')
    reviews = 'позже добавить отзывы'

    if len(article_number) > 1:
        article_info = article_number[2].get_text(strip=True)
        article = re.sub(r'[a-zA-Zа-яА-ЯёЁ]', '', article_info)
        article = article.replace(': ', '')
        print(f'Артикул: {article}')
    else:
        print("Элемент 'article_number' не найден")

    if name_products:
        product_title = name_products.get_text(strip=True)
        print(f'Название товара: {product_title}')
    else:
        print("Элемент 'name_products' не найден")

    if rating:
        original_string_rating = rating.get_text(strip=True)
        if "." in original_string_rating:
            product_rating = original_string_rating[:3]
        else:
            product_rating = original_string_rating[:1]
        print(f'Рейтинг товара: {product_rating}')
    else:
        print("Элемент 'rating' не найден")

    if price:
        original_string_price = price.get_text(strip=True)
        product_price = original_string_price[:-1]
        print(f'Цена товара: {product_price}')
    else:
        print("Элемент 'price' не найден")

    def extract_image_urls(img_tag, base_url):
        urls = set()

        src = img_tag.get('src')
        if src and not src.startswith('data:image'):
            high_res_src = src.replace('/wc50/', '/wc1000/').replace('/wc100/', '/wc1000/')
            urls.add(urljoin(base_url, high_res_src))

        srcset = img_tag.get('srcset')
        if srcset:
            for source in srcset.split(','):
                parts = source.strip().split(' ')
                if len(parts) >= 1:
                    url_part = parts[0]
                    high_res_url = url_part.replace('/wc50/', '/wc1000/')
                    high_res_url = high_res_url.replace('/wc100/', '/wc1000/')
                    urls.add(urljoin(base_url, high_res_url))

        return urls


    all_image_urls = set()
    main_container = soup.find('div', class_='lm9_28')
    if not main_container:
        print("ОШИБКА: Контейнер 'lm9_28' не найден!")

    if main_container:
        image_blocks = main_container.find_all('div', class_='ml5_28', attrs={"data-index": True})
        for block in image_blocks:
            img_container = block.find('div', class_='j8z_28')
            if img_container:
                img_div = img_container.find('div', class_='k1o_28')
                if img_div:
                    img_tag = img_div.find('img', class_='z9j_28 b933-a')
                    if img_tag:
                        urls = extract_image_urls(img_tag, "https://www.ozon.ru")
                        all_image_urls.update(urls)

    print("Изображения товара:")
    if all_image_urls:
        for id, url in enumerate(all_image_urls, 1):
            print(f"[{id}] {url}")
    else:
        print("Изображения не найдены!")





#get_products_data_Ozon()
