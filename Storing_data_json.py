import json
import os


def Storing_data_Ozon(link_products, article, title, price, rating, reviews, image_urls, user_ip):
    product_data = {
        "link_products": link_products,
        "article": article,
        "title": title,
        "price": price,
        "rating": rating,
        "reviews": reviews,
        "image_urls": image_urls
    }

    filename = f"json products data/{user_ip}-Ozon.json"
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


def Storing_data_WB(link_products, article, title, price, rating, reviews, image_urls, user_ip):
    product_data = {
        "link_products": link_products,
        "article": article,
        "title": title,
        "price": price,
        "rating": rating,
        "reviews": reviews,
        "image_urls": image_urls
    }

    filename = f"json products data/{user_ip}-WB.json"
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


def Storing_data_YandexMarket(link_products, article, title, price, rating, reviews, image_urls, user_ip):
    product_data = {
        "link_products": link_products,
        "article": article,
        "title": title,
        "price": price,
        "rating": rating,
        "reviews": reviews,
        "image_urls": image_urls
    }

    filename = f"json products data/{user_ip}-YandexMarket.json"
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


def Storing_data_MagnitMarket(link_products, title, price, rating, reviews, image_urls, user_ip):
    product_data = {
        "link_products": link_products,
        "title": title,
        "price": price,
        "rating": rating,
        "reviews": reviews,
        "image_urls": image_urls
    }

    filename = f"json products data/{user_ip}-MagnitMarket.json"
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


def Storing_data_DNS(link_products, article, title, price, rating, reviews, image_urls, user_ip):
    product_data = {
        "link_products": link_products,
        "article": article,
        "title": title,
        "price": price,
        "rating": rating,
        "reviews": reviews,
        "image_urls": image_urls
    }

    filename = f"json products data/{user_ip}-DNS.json"
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


def Storing_data_Citilink(link_products, article, title, price, rating, reviews, image_urls, user_ip):
    product_data = {
        "link_products": link_products,
        "article": article,
        "title": title,
        "price": price,
        "rating": rating,
        "reviews": reviews,
        "image_urls": image_urls
    }

    filename = f"json products data/{user_ip}-Citilink.json"
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


def Storing_data_M_Video(link_products, article, title, price, rating, reviews, image_urls, user_ip):
    product_data = {
        "link_products": link_products,
        "article": article,
        "title": title,
        "price": price,
        "rating": rating,
        "reviews": reviews,
        "image_urls": image_urls
    }

    filename = f"json products data/{user_ip}-M_Video.json"
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


# def Storing_data_Avito(link_products, article, title, price, rating, reviews, image_urls, user_id):
#
#
# def Storing_data_Youla(link_products, article, title, price, rating, reviews, image_urls, user_id):


def Storing_data_Aliexpress(link_products, title, price, rating, reviews, image_urls, user_ip):
    product_data = {
        "link_products": link_products,
        "title": title,
        "price": price,
        "rating": rating,
        "reviews": reviews,
        "image_urls": image_urls
    }

    filename = f"json products data/{user_ip}-Aliexpress.json"
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


def Storing_data_Joom(link_products, title, price, rating, reviews, image_urls, user_ip):
    product_data = {
        "link_products": link_products,
        "title": title,
        "price": price,
        "rating": rating,
        "reviews": reviews,
        "image_urls": image_urls
    }

    filename = f"json products data/{user_ip}-Joom.json"
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


def Storing_data_Shop_mts(link_products, article, title, price, rating, reviews, image_urls, user_ip):
    product_data = {
        "link_products": link_products,
        "article": article,
        "title": title,
        "price": price,
        "rating": rating,
        "reviews": reviews,
        "image_urls": image_urls
    }

    filename = f"json products data/{user_ip}-Shop_mts.json"
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


def Storing_data_Technopark(link_products, article, title, price, rating, reviews, image_urls, user_ip):
    product_data = {
        "link_products": link_products,
        "article": article,
        "title": title,
        "price": price,
        "rating": rating,
        "reviews": reviews,
        "image_urls": image_urls
    }

    filename = f"json products data/{user_ip}-Technopark.json"
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


def Storing_data_Lamoda(link_products, article, title, price, rating, reviews, image_urls, user_ip):
    product_data = {
        "link_products": link_products,
        "article": article,
        "title": title,
        "price": price,
        "rating": rating,
        "reviews": reviews,
        "image_urls": image_urls
    }

    filename = f"json products data/{user_ip}-Lamoda.json"
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





