import json
import os


def Storing_data_Ozon(article, title, price, rating, reviews, image_urls, user_id):
    product_data = {
        "article": article,
        "title": title,
        "price": price,
        "rating": rating,
        "reviews": reviews,
        "image_urls": image_urls
    }

    filename = f"json products data/{user_id}-Ozon.json"
    data = []

    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []

    data.append(product_data)

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def Storing_data_WB(article, title, price, rating, reviews, image_urls, user_id):
    product_data = {
        "article": article,
        "title": title,
        "price": price,
        "rating": rating,
        "reviews": reviews,
        "image_urls": image_urls
    }

    filename = f"json products data/{user_id}-WB.json"
    data = []

    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []

    data.append(product_data)

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def Storing_data_YandexMarket(article, title, price, rating, reviews, image_urls, user_id):
    product_data = {
        "article": article,
        "title": title,
        "price": price,
        "rating": rating,
        "reviews": reviews,
        "image_urls": image_urls
    }

    filename = f"json products data/{user_id}-YandexMarket.json"
    data = []

    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []

    data.append(product_data)

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def Storing_data_MagnitMarket(title, price, rating, reviews, image_urls, user_id):
    product_data = {
        "title": title,
        "price": price,
        "rating": rating,
        "reviews": reviews,
        "image_urls": image_urls
    }

    filename = f"json products data/{user_id}-MagnitMarket.json"
    data = []

    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []

    data.append(product_data)

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)