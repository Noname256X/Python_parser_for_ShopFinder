import json
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import os
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time


def get_products_data_Ozon(link_products, driver):
    print(f'Ссылка на товар:{link_products}')

    def get_product_article(driver):
        try:
            element_article = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[contains(., 'Артикул:')]")
                )
            )

            full_text_article = element_article.text
            return re.search(r'Артикул:\s*(\d+)', full_text_article)

        except Exception as e:
            print(f"Ошибка при поиске артикула: {str(e)}")
            return None

    def get_product_title(driver):
        try:
            container = WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//div[@data-widget='webProductHeading']")
                )
            )

            h1_element = container.find_element(By.TAG_NAME, 'h1')
            return h1_element.text.strip().replace('\n', ' ')

        except Exception as e:
            print(f"Ошибка при поиске заголовка: {str(e)}")
            return None

    def get_product_price(driver):
        try:
            element_price = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//div[@data-widget='webPrice']//span[contains(., '₽')]")
                )
            )

            if  'c Ozon Картой' in element_price[0].text:
                return element_price[2].text
            elif 'c Ozon Картой' in element_price[1].text:
                return element_price[3].text
            else:
                return None

        except Exception as e:
            print(f"Ошибка при поиске цены: {str(e)}")
            return None

    def get_product_rating_reviews(driver):
        try:
            rating_block = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@data-widget='webSingleProductScore']")
                )
            )

            rating_text = rating_block.find_element(
                By.XPATH, ".//div[contains(@class, 'tsBodyControl500Medium')]"
            ).text

            rating, reviews = rating_text.split(" • ")
            reviews = reviews.replace(' отзывов','').replace(' отзыва','').replace(' отзыв', '')
            return rating, reviews

        except Exception as e:
            print(f"Ошибка получения рейтинга: {str(e)}")
            return None

    def get_product_images(driver):
        try:
            gallery = WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//div[@data-widget='webGallery']")
                )
            )
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", gallery)

            image_blocks = WebDriverWait(gallery, 10).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, ".//div[contains(@class, 'm6k_28') and .//img[contains(@src, 'ir-')]]")
                )
            )

            images = []
            for block in image_blocks:
                try:
                    img = WebDriverWait(block, 5).until(
                        EC.visibility_of_element_located(
                            (By.XPATH, ".//img[contains(@src, 'ir-')]")
                        )
                    )

                    src = img.get_attribute('src')
                    if '/wc50/' in src:
                        hd_src = src.replace('/wc50/', '/wc1000/')
                    else:
                        hd_src = src.split('?')[0]

                    images.append(hd_src)

                except Exception as e:
                    print(f"Пропущен блок: {e}")
                    continue

            return list(set(images))

        except Exception as e:
            print(f"Ошибка парсинга галереи: {str(e)}")
            return []


    article = get_product_article(driver)
    title = get_product_title(driver)
    price = get_product_price(driver)
    rating, reviews = get_product_rating_reviews(driver)
    image_urls = get_product_images(driver)


    if article:
        print(f'Артикул: {article.group(1)}')
    else:
        print(f'Артикул: None')

    if title:
        print(f"Заголовок товара: {title}")
    else:
        print("Заголовок товара: None")

    if price:
        print(f'Цена товара: {price}')
    else:
        print(f'Цена на товара: None')

    if rating:
        print(f'Рейтинг: {rating}')
    else:
        print('Рейтинг: None')

    if reviews:
        print(f'Отзывы: {reviews}')
    else:
        print('Отзывы: None')

    for idx, url in enumerate(image_urls, 1):
        print(f"Изображение {idx}: {url}")

    print('-----------------------------')


def get_products_data_WB(link_products, driver):
    print(f'Ссылка на товар:{link_products}')

    def get_product_article(driver):
        try:
            element_article = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[contains(., 'Артикул')]")
                )
            )

            full_text_article = element_article.text
            return re.search(r'Артикул\s*(\d+)', full_text_article)

        except Exception as e:
            print(f"Ошибка при поиске артикула: {str(e)}")
            return None

    def get_product_title(driver):
        try:
            title_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//h1[@class='product-page__title']"))
            )

            return title_element.text.strip()

        except Exception as e:
            print(f"Ошибка при получении название товара: {e}")
            return None

    def get_product_price(driver):
        try:
            price_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "ins.price-block__final-price.wallet")
                )
            )

            price_text = price_element.get_attribute('textContent').replace('\xa0', ' ').strip().replace(' ₽', '')

            return price_text

        except Exception as e:
            print(f"Ошибка при получении цены: {e}")
            return None

    def get_product_rating_reviews(driver):
        try:
            rating_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "span.product-review__rating.address-rate-mini")
                )
            )

            reviews_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "span.product-review__count-review.j-wba-card-item-show")
                )
            )

            rating = rating_element.text.strip().replace(',', '.')
            reviews = reviews_element.text.replace('\xa0', ' ').replace(' оценок','').replace(' оценки','')
            return rating, reviews

        except Exception as e:
            print(f"Ошибка получения рейтинга: {str(e)}")
            return None

    def get_high_res_image_url(url):
        if '/c246x328/' in url:
            return url.replace('/c246x328/', '/big/')
        elif '/tm/' in url:
            return url.replace('/tm/', '/big/')
        return url

    def get_product_images(driver, article):
        try:
            img_elements = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//img[contains(@src, 'wbbasket.ru') or contains(@data-src-pb, 'wbbasket.ru')]")
                )
            )

            images = []
            pattern = re.compile(rf'.*/vol\d+/part\d+/{article}/.*')

            for img in img_elements:
                img_url = img.get_attribute('data-src-pb') or img.get_attribute('src')

                if img_url and pattern.search(img_url):
                    hi_res_url = get_high_res_image_url(img_url)
                    images.append(hi_res_url)

            return list(set(images))

        except Exception as e:
            print(f"Ошибка парсинга изображений: {str(e)}")
            return []


    article = get_product_article(driver)
    title = get_product_title(driver)
    price = get_product_price(driver)
    rating, reviews = get_product_rating_reviews(driver)
    image_urls = get_product_images(driver, article.group(1))


    if article:
        print(f'Артикул: {article.group(1)}')
    else:
        print(f'Артикул: None')

    if title:
        print(f"Заголовок товара: {title}")
    else:
        print("Заголовок товара: None")

    if price:
        print(f'Цена товара: {price}')
    else:
        print(f'Цена товара: None')

    if rating:
        print(f'Рейтинг: {rating}')
    else:
        print('Рейтинг: None')

    if reviews:
        print(f'Отзывы: {reviews}')
    else:
        print('Отзывы: None')

    print(f"Найдено изображений: {len(image_urls)}")
    for img in image_urls:
        print(img)

    print('-----------------------------')


def get_products_data_YandexMarket(link_products, driver):
    print(f'Ссылка на товар:{link_products}')

    def get_product_article(driver):
        try:
            article_element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[normalize-space()='Артикул Маркета']/following-sibling::div//span"))
            )

            return article_element.text.strip()

        except Exception as e:
            print(f"Не удалось найти артикул: {str(e)}")
            return None

    def get_product_title(driver):
        try:
            title_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//h1[@data-auto='productCardTitle']")
                )
            )

            return title_element.text

        except Exception as e:
            print(f"Не удалось найти артикул: {str(e)}")
            return None

    def get_product_price(driver):
        try:
            price_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     "//span[@class='ds-visuallyHidden' and contains(text(), 'Цена с картой Яндекс Пэй')]/following::span[contains(@class, 'ds-text_color_price-term')][1]")
                )
            )

            return price_element.text.replace('\u202f', '')

        except Exception as e:
            print(f"Ошибка при получении цены: {str(e)}")
            return None

    def get_product_rating_reviews(driver):
        try:
            rating_element = WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, '[data-auto="ratingValue"]')
                )
            )
            reviews_element = WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, '[data-auto="ratingCount"]')
                )
            )

            rating = rating_element.text
            reviews = reviews_element.text.replace('(', '').replace(')', '')
            return rating, reviews

        except Exception as e:
            print(f"Ошибка при получении рейтинга или отзывов: {e}")
            print(f'Этот товар не будет добавлен')
            return


    article = get_product_article(driver)
    title = get_product_title(driver)
    price = get_product_price(driver)
    rating, reviews = get_product_rating_reviews(driver)


    print(f'Артикул: {article}')
    print(f'Заголовок товара: {title}')
    print(f'Цена товара: {price}')
    print(f'Рейтинг: {rating}')
    print(f'Отзывы: {reviews}')

    print('-----------------------------')