import json
import os


def Storing_data_Ozon(link_products, article, title, price, rating, reviews, image_urls, user_id):
    product_data = {
        "link_products": link_products,
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


def Storing_data_WB(link_products, article, title, price, rating, reviews, image_urls, user_id):
    product_data = {
        "link_products": link_products,
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


def Storing_data_YandexMarket(link_products, article, title, price, rating, reviews, image_urls, user_id):
    product_data = {
        "link_products": link_products,
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


def Storing_data_MagnitMarket(link_products, title, price, rating, reviews, image_urls, user_id):
    product_data = {
        "link_products": link_products,
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


def Storing_data_DNS(link_products, article, title, price, rating, reviews, image_urls, user_id):
    product_data = {
        "link_products": link_products,
        "article": article,
        "title": title,
        "price": price,
        "rating": rating,
        "reviews": reviews,
        "image_urls": image_urls
    }

    filename = f"json products data/{user_id}-DNS.json"
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


def Storing_data_Citilink(link_products, article, title, price, rating, reviews, image_urls, user_id):
    product_data = {
        "link_products": link_products,
        "article": article,
        "title": title,
        "price": price,
        "rating": rating,
        "reviews": reviews,
        "image_urls": image_urls
    }

    filename = f"json products data/{user_id}-Citilink.json"
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