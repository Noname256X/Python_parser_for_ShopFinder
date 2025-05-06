import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, TimeoutException
import os
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse, urlunparse
import time
from Storing_data_json import *
import random
from dotenv import load_dotenv


def get_products_data_Ozon(link_products, driver, user_id):
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
            container = WebDriverWait(driver, 10).until(
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
            rating_block = WebDriverWait(driver, 10).until(
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
            return None, None

    def get_product_images(driver):
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@data-widget="webGallery"]'))
            )

            gallery = driver.find_element(By.XPATH, '//div[@data-widget="webGallery"]')
            driver.execute_script("arguments[0].scrollIntoView();", gallery)

            images = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, '//div[@data-widget="webGallery"]//div[@data-index]//img')
                )
            )

            image_urls = set()

            for img in images:
                src = img.get_attribute("src") or ""
                srcset = img.get_attribute("srcset") or ""

                best_src = ""
                if srcset:
                    sources = [s.strip() for s in srcset.split(",")]
                    sources.sort(key=lambda x: int(x.split()[-1][:-1]), reverse=True)
                    best_src = sources[0].split()[0] if sources else ""

                final_url = best_src if best_src else src

                if final_url and "ir-8.ozone.ru/s3/" in final_url and "cover" not in final_url:
                    if "wc100" in final_url:
                        final_url = final_url.replace("wc100", "wc2000")
                    elif "wc50" in final_url:
                        final_url = final_url.replace("wc50", "wc2000")

                    image_urls.add(final_url)

            return list(image_urls)

        except Exception as e:
            print(f"Ошибка парсинга изображений: {str(e)}")
            return []


    article = get_product_article(driver)
    title = get_product_title(driver)
    price = get_product_price(driver)
    rating, reviews = get_product_rating_reviews(driver)
    image_urls = get_product_images(driver)

    if article and title and price and rating and reviews and image_urls != None:
        print(f'Артикул: {article.group(1)}')
        print(f'Заголовок товара: {title}')
        print(f'Цена товара: {price}')
        print(f'Рейтинг: {rating}')
        print(f'Отзывы: {reviews}')
        print(f"Найдено изображений: {len(image_urls)}")

        for i in range(len(image_urls)):
            print(f'{i + 1}: {image_urls[i]}')

        Storing_data_Ozon(link_products, article.group(1), title, price, rating, reviews, image_urls, user_id)
    else:
        print(f'Этот товар не будет добавлен в json-файл')

    print('-----------------------------')


def get_products_data_WB(link_products, driver, user_id):
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
            return None, None

    def get_high_res_image_url(url):
        if '/c246x328/' in url:
            return url.replace('/c246x328/', '/big/')
        elif '/tm/' in url:
            return url.replace('/tm/', '/big/')
        return url

    def get_product_images(driver, article):
        try:
            img_elements = WebDriverWait(driver, 10).until(
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

    if article and title and price and rating and reviews and image_urls != None:
        print(f'Артикул: {article.group(1)}')
        print(f'Заголовок товара: {title}')
        print(f'Цена товара: {price}')
        print(f'Рейтинг: {rating}')
        print(f'Отзывы: {reviews}')
        print(f"Найдено изображений: {len(image_urls)}")

        for i in range(len(image_urls)):
            print(f'{i + 1}: {image_urls[i]}')

        Storing_data_WB(link_products, article.group(1), title, price, rating, reviews, image_urls, user_id)
    else:
        print(f'Этот товар не будет добавлен в json-файл')

    print('-----------------------------')


def get_products_data_YandexMarket(link_products, driver, user_id):
    print(f'Ссылка на товар:{link_products}')

    def get_product_article(driver):
        try:
            article_element = WebDriverWait(driver, 10).until(
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
            rating_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, '[data-auto="ratingValue"]')
                )
            )
            reviews_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, '[data-auto="ratingCount"]')
                )
            )

            rating = rating_element.text
            reviews = reviews_element.text.replace('(', '').replace(')', '')
            return rating, reviews

        except Exception as e:
            print(f"Ошибка при получении рейтинга или отзывов: {e}")
            return None, None

    def get_product_images(driver):
        try:
            thumbnails_list = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//ul[@data-auto='media-viewer-thumbnails']"))
            )

            li_elements = thumbnails_list.find_elements(By.TAG_NAME, "li")

            image_urls = []
            for li in li_elements:
                img = WebDriverWait(li, 2).until(
                    EC.presence_of_element_located((By.TAG_NAME, "img"))
                )
                src = img.get_attribute("src")
                if src:
                    image_urls.append(src)

            return image_urls

        except Exception as e:
            print(f"Ошибка парсинга изображений: {str(e)}")
            return []


    article = get_product_article(driver)
    title = get_product_title(driver)
    price = get_product_price(driver)
    rating, reviews = get_product_rating_reviews(driver)
    image_urls = get_product_images(driver)

    if article and title and price and rating and reviews and image_urls != None:
        print(f'Артикул: {article}')
        print(f'Заголовок товара: {title}')
        print(f'Цена товара: {price}')
        print(f'Рейтинг: {rating}')
        print(f'Отзывы: {reviews}')
        print(f"Найдено изображений: {len(image_urls)}")

        for i in range(len(image_urls)):
            print(f'{i + 1}: {image_urls[i]}')

        Storing_data_YandexMarket(link_products, article, title, price, rating, reviews, image_urls, user_id)
    else:
        print(f'Этот товар не будет добавлен в json-файл')

    print('-----------------------------')


def get_products_data_MagnitMarket(link_products, driver, user_id):
    print(f'Ссылка на товар:{link_products}')

    def get_product_title(driver):
        try:
            product_name_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "h1[data-test-id='text__product-name']")
                )
            )

            return product_name_element.text

        except Exception as e:
            print(f"Не удалось найти название товара: {str(e)}")
            return None


    def get_product_price(driver):
        try:
            price_element = driver.find_element(By.CSS_SELECTOR, '[data-test-id="text__product-price"]')

            return price_element.text.replace(' ₽', '')

        except Exception as e:
            print(f"Ошибка при получении цены: {str(e)}")
            return None


    def get_product_rating_reviews(driver):
        try:
            rating_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//span[@data-test-id='text__product-rating' and contains(@class, 'rating-value')]")
                )
            )

            reviews_element = driver.find_element(
                By.XPATH, '//span[@data-test-id="text__quantity-of-reviews"]'
            )

            rating = rating_element.text
            reviews = reviews_element.text.strip().replace('(', '').replace(')','').replace(' отзыва', '').replace(' отзывов', '').replace(' отзыв', '')

            return rating, reviews


        except Exception as e:
            print(f"Ошибка при получении рейтинга или отзывов: {e}")
            return None, None


    def get_product_images(driver):
        try:
            photos = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "div[data-test-id='list__vertical-photo-carousel'] img")
                )
            )

            image_urls = []
            for img in photos:
                src = img.get_attribute("src")
                if not src:
                    continue

                # Парсим URL для обработки пути
                parsed_url = urlparse(src)
                path_parts = parsed_url.path.split('/')

                if not path_parts:
                    continue

                path_parts[-1] = "original.jpg"
                new_path = '/'.join(path_parts)

                new_parsed = parsed_url._replace(path=new_path, query="", fragment="")
                high_res_url = urlunparse(new_parsed)

                image_urls.append(high_res_url)

            return list(set(image_urls))

        except Exception as e:
            print(f"Ошибка парсинга изображений: {str(e)}")
            return []


    title = get_product_title(driver)
    price = get_product_price(driver)
    rating, reviews = get_product_rating_reviews(driver)
    image_urls = get_product_images(driver)

    if title and price and rating and reviews and image_urls != None:
        print(f'Заголовок товара: {title}')
        print(f'Цена товара: {price}')
        print(f'Рейтинг: {rating}')
        print(f'Отзывы: {reviews}')
        print(f"Найдено изображений: {len(image_urls)}")

        for i in range(len(image_urls)):
            print(f'{i + 1}: {image_urls[i]}')

        Storing_data_MagnitMarket(link_products, title, price, rating, reviews, image_urls, user_id)
    else:
        print(f'Этот товар не будет добавлен в json-файл')

    print('-----------------------------')


def get_products_data_DNS(link_products, driver, user_id):
    print(f'Ссылка на товар:{link_products}')

    def get_product_article(driver):
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "product-card-top__code")]'))
            )

            return element.text

        except Exception as e:
            print(f"Не удалось найти артикул: {str(e)}")
            return None


    def get_product_title(driver):
        try:
            title_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//h1[contains(@class, "product-card-top__title")]'))
            )

            return title_element.text.strip()

        except Exception as e:
            print(f"Не удалось найти название товара: {str(e)}")
            return None


    def get_product_price(driver):
        try:
            price_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "product-buy__price")]'))
            )

            price_text = price_element.text.split('₽')[0].strip()

            return price_text.replace('&nbsp;', ' ')

        except Exception as e:
            print(f"Ошибка при получении цены: {str(e)}")
            return None


    def get_product_rating_reviews(driver):
        try:
            rating_container = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a.product-card-top__rating'))
            )

            full_text = rating_container.text

            rating = re.search(r'(\d+\.\d+)', full_text).group(1)

            reviews_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//a[contains(@class, "product-card-top__rating")]'))
            )

            full_text = reviews_element.text

            reviews_match = re.search(r'(\d+[\d,.]*(?:[кk]|тыс)?)\s*отзыв[а-яё]*', full_text, re.IGNORECASE)

            reviews = reviews_match.group(1) if reviews_match else None

            return rating, reviews

        except Exception as e:
            print(f"Ошибка при получении рейтинга или отзывов: {e}")
            return None, None


    def get_product_images(driver): # Пересмотреть решение
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "img.product-images-slider__img"))
            )

            images = driver.find_elements(By.CSS_SELECTOR, 'img.product-images-slider__img')

            image_urls = []
            for img in images:
                url = img.get_attribute('src') or img.get_attribute('data-src')
                if url and url.startswith('http'):
                    image_urls.append(url)

            seen = set()
            return [x for x in image_urls if not (x in seen or seen.add(x))]

        except Exception as e:
            print(f"Ошибка парсинга изображений: {str(e)}")
            return []


    article = get_product_article(driver)
    title = get_product_title(driver)
    price = get_product_price(driver)
    rating, reviews = get_product_rating_reviews(driver)
    image_urls = get_product_images(driver)

    if title and price and rating and reviews and image_urls != None:
        print(f'Заголовок товара: {title}')
        print(f'Цена товара: {price}')
        print(f'Рейтинг: {rating}')
        print(f'Отзывы: {reviews}')
        print(f"Найдено изображений: {len(image_urls)}")

        for i in range(len(image_urls)):
            print(f'{i + 1}: {image_urls[i]}')

        Storing_data_DNS(link_products, article, title, price, rating, reviews, image_urls[0], user_id)
    else:
        print(f'Этот товар не будет добавлен в json-файл')

    print('-----------------------------')


def get_products_data_Citilink(link_products, driver, user_id):
    print(f'Ссылка на товар:{link_products}')

    def get_product_article(driver):
        try:
            article_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Код товара:")]//button'))
            )

            return article_element.text

        except Exception as e:
            print(f"Не удалось найти артикул: {str(e)}")
            return None


    def get_product_title(driver):
        try:
            title_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'h1'))
            )

            return title_element.text

        except Exception as e:
            print(f"Не удалось найти название товара: {str(e)}")
            return None


    def get_product_price(driver):
        try:
            price_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//span[contains(@class, "MainPriceNumber")]'))
            )

            price = int(price_element.text)

            if price >= 1000:
                return f"{price:,}".replace(",", " ")
            return str(price)

        except Exception as e:
            print(f"Ошибка при получении цены: {str(e)}")
            return None


    def get_product_rating_reviews(driver):
        try:
            rating_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH,
                                                "//*[contains(text(), 'Рейтинг товара')]/following::span[contains(@class, 'StyledTypography')]"))
            )

            rating = rating_element.text

            reviews_tab = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'otzyvy')]"))
            )

            reviews_count = reviews_tab.find_element(
                By.XPATH, ".//span[contains(@class, 'CountWrapper')]"
            )

            reviews = reviews_count.text

            return rating, reviews

        except Exception as e:
            print(f"Ошибка при получении рейтинга или отзывов: {e}")
            return None, None


    def get_product_images(driver): #Доработать (парсится 1 картинка товара)
        try:
            main_image = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.is-selected[data-meta-id^='GallerySlide']"))
            )
            main_image.click()

            image_urls = []

            large_image = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "div.app-catalog-jeajt7-StyledImageWrapper img"))
            )
            current_url = large_image.get_attribute("src")

            image_urls.append(current_url)

            return image_urls

        except Exception as e:
            print(f"Ошибка при получении изображений: {str(e)}")
            return []


    article = get_product_article(driver)
    title = get_product_title(driver)
    price = get_product_price(driver)
    rating, reviews = get_product_rating_reviews(driver)
    image_urls = get_product_images(driver)

    if article and title and price and rating and reviews and image_urls != None:
        print(f'Артикул: {article}')
        print(f'Заголовок товара: {title}')
        print(f'Цена товара: {price}')
        print(f'Рейтинг: {rating}')
        print(f'Отзывы: {reviews}')
        print(f"Найдено изображений: {len(image_urls)}")

        for i in range(len(image_urls)):
            print(f'{i + 1}: {image_urls[i]}')

        Storing_data_Citilink(link_products, article, title, price, rating, reviews, image_urls, user_id)
    else:
        print(f'Этот товар не будет добавлен в json-файл')

    print('-----------------------------')


def get_products_data_M_Video(link_products, driver, user_id):
    print(f'Ссылка на товар:{link_products}')

    def get_product_article(driver):
        try:
            article_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//div[contains(@class, 'product-code-container')]//span[@mvidremovespaces]"))
            )

            return article_element.text.replace('\u00a0', '')

        except Exception as e:
            print(f"Не удалось найти артикул: {str(e)}")
            return None


    def get_product_title(driver):
        try:
            title_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//div[contains(@class, 'details')]//h1[contains(@class, 'title')]"))
            )

            return title_element.text.strip()


        except Exception as e:
            print(f"Не удалось найти название товара: {str(e)}")
            return None


    def get_product_price(driver):
        try:
            price_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH,
                                                  "//div[contains(@class, 'specs-price__grid')]//span[contains(@class, 'price__main-value')]"))
            )

            return price_element.text.strip().replace(' ₽','')

        except Exception as e:
            print(f"Ошибка при получении цены: {str(e)}")
            return None


    def get_product_rating_reviews(driver):
        try:
            actions = ActionChains(driver)

            for i in range(random.randint(5, 7)):
                time.sleep(random.randint(1, 3))
                actions.send_keys(Keys.PAGE_DOWN).perform()

            reviews_block = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#PRODUCTS_REVIEWS_BLOCK_ID"))
            )

            rating_element = reviews_block.find_element(By.CSS_SELECTOR, "span[class*='rating-value']")
            rating = rating_element.text

            reviews_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH,
                '//div[contains(@class, "review-share-code")]'
                '//a[contains(@class, "rating-reviews") and contains(text(), "отзыв")]'))
            )

            reviews_text = reviews_element.text
            reviews = int(reviews_text.split()[0])

            return rating, reviews

        except Exception as e:
            print(f"Ошибка при получении рейтинга или отзывов: {e}")
            return None, None


    def get_product_images(driver):
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "mvid-items-track"))
            )

            items = driver.find_elements(By.CSS_SELECTOR, "mvid-items-track div.item")
            image_urls = []

            for item in items:
                img = item.find_element(By.CSS_SELECTOR, "img.item-img")
                src = img.get_attribute("src")

                if src.startswith("//"):
                    src = f"https:{src}"
                high_res_src = src.replace("/small_pic/200/", "/")
                image_urls.append(high_res_src)

            return image_urls

        except Exception as e:
            print(f"Ошибка при получении изображений: {str(e)}")
            return []


    article = get_product_article(driver)
    title = get_product_title(driver)
    price = get_product_price(driver)
    rating, reviews = get_product_rating_reviews(driver)
    image_urls = get_product_images(driver)

    if article and title and price and rating and reviews and image_urls != None:
        print(f'Артикул: {article}')
        print(f'Заголовок товара: {title}')
        print(f'Цена товара: {price}')
        print(f'Рейтинг: {rating}')
        print(f'Отзывы: {reviews}')
        print(f"Найдено изображений: {len(image_urls)}")

        for i in range(len(image_urls)):
            print(f'{i + 1}: {image_urls[i]}')

        Storing_data_M_Video(link_products, article, title, price, rating, reviews, image_urls, user_id)
    else:
        print(f'Этот товар не будет добавлен в json-файл')

    print('-----------------------------')


# def get_products_data_Avito(link_products, driver, user_id):
#     print(f'Ссылка на товар:{link_products}')


# def get_products_data_Youla(link_products, driver, user_id):
#     print(f'Ссылка на товар:{link_products}')


def get_products_data_Aliexpress(link_products, driver, user_id):
    print(f'Ссылка на товар:{link_products}')

    def get_product_title(driver):
        try:
            title_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//div[@data-product-description="true"]//h1'))
            )

            return title_element.text

        except Exception as e:
            print(f"Не удалось найти название товара: {str(e)}")
            return None


    def get_product_price(driver):
        try:
            price_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//div[contains(@class, "HazeProductPrice_SnowPrice__mainS__")]')
                )
            )

            return price_element.text.replace('&nbsp;', ' ')

        except Exception as e:
            print(f"Ошибка при получении цены: {str(e)}")
            return None


    def get_product_rating_reviews(driver):
        try:
            rating_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH,
                     '//div[@data-spm="title_floor"]//span[contains(@class, "red-ali-kit_Typography") and contains(@class, "red-ali-kit_Body__M__1bdiye")]')
                )
            )

            rating = rating_element.text

            reviews_element = driver.find_element(
                By.XPATH,
                '//p[contains(@class, "RedReviewsProductRatingOld_MainSection__allReviewsLinkTitle") and contains(text(), "отзыв")]'
            )

            reviews_text = reviews_element.text
            reviews = int(re.sub(r'\D', '', reviews_text))

            return rating, reviews

        except Exception as e:
            print(f"Ошибка при получении рейтинга или отзывов: {e}")
            return None, None


    def get_product_images(driver):
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'SnowProductGallery__previewItem')]"))
            )

            photo_blocks = driver.find_elements(
                By.XPATH, "//div[contains(@class, 'SnowProductGallery__previewItem')]//picture"
            )

            image_urls = []
            for block in photo_blocks:
                img = block.find_element(By.TAG_NAME, "img")
                src = img.get_attribute("src")
                if src:
                    image_urls.append(src)

            return image_urls

        except Exception as e:
            print(f"Ошибка при получении изображений: {str(e)}")
            return []

    title = get_product_title(driver)
    price = get_product_price(driver)
    rating, reviews = get_product_rating_reviews(driver)
    image_urls = get_product_images(driver)

    if title and price and rating and reviews and image_urls != None:
        print(f'Заголовок товара: {title}')
        print(f'Цена товара: {price}')
        print(f'Рейтинг: {rating}')
        print(f'Отзывы: {reviews}')
        print(f"Найдено изображений: {len(image_urls)}")

        for i in range(len(image_urls)):
            print(f'{i + 1}: {image_urls[i]}')

        Storing_data_Aliexpress(link_products, title, price, rating, reviews, image_urls, user_id)
    else:
        print(f'Этот товар не будет добавлен в json-файл')

    print('-----------------------------')


def get_products_data_Joom(link_products, driver, user_id):
    print(f'Ссылка на товар:{link_products}')

    def get_product_title(driver):
        try:
            elements = driver.find_elements('css selector', 'span.expandButton___YkTmW[role="button"][tabindex="0"]')

            if elements:
                element = elements[0]
                element.click()

            title_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//h1[contains(@class, "root___e0mAF")]'))
            )

            full_text = title_element.get_attribute('textContent').strip()
            return full_text.split('…')[0].strip()

        except Exception as e:
            print(f"Не удалось найти название товара: {str(e)}")
            return None


    def get_product_price(driver):
        try:
            price_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH,
                                                  "//div[contains(@class, 'priceWrap') and contains(@class, 'regular')]//div[contains(@class, 'price')]/span[not(@class)]"))
            )

            return price_element.text.replace('\xa0', ' ')

        except Exception as e:
            print(f"Ошибка при получении цены: {str(e)}")
            return None


    def get_product_rating_reviews(driver):
        try:
            rating_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//h3[contains(., "Отзывы")]/following-sibling::div//div[contains(@class, "label___")]'))
            )

            rating = rating_element.text

            reviews_count_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//h3[contains(., 'Отзывы')]/span/span[last()]")
                )
            )

            reviews = int(reviews_count_element.text)

            return rating, reviews

        except Exception as e:
            print(f"Ошибка при получении рейтинга или отзывов: {e}")
            return None, None


    def get_product_images(driver):
        try:
            thumbnails = WebDriverWait(driver, 15).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, 'button[class*="thumb___"]')
                )
            )

            image_urls = []

            for thumbnail in thumbnails:
                try:
                    img = thumbnail.find_element(By.TAG_NAME, 'img')
                    srcset = img.get_attribute('srcset')

                    if srcset:
                        urls = [url.strip().split()[0] for url in srcset.split(',')]
                        original_url = urls[-1] if urls else None

                        if original_url:
                            image_urls.append(original_url)
                except Exception as e:
                    print(f"Ошибка при обработке элемента: {e}")

            return image_urls

        except Exception as e:
            print(f"Ошибка при получении изображений: {str(e)}")
            return []

    title = get_product_title(driver)
    price = get_product_price(driver)
    rating, reviews = get_product_rating_reviews(driver)
    image_urls = get_product_images(driver)

    if title and price and rating and reviews:
        print(f'Заголовок товара: {title}')
        print(f'Цена товара: {price}')
        print(f'Рейтинг: {rating}')
        print(f'Отзывы: {reviews}')
        print(f"Найдено изображений: {len(image_urls)}")

        for i in range(len(image_urls)):
            print(f'{i + 1}: {image_urls[i]}')

        Storing_data_Joom(link_products, title, price, rating, reviews, image_urls, user_id)
    else:
        print(f'Этот товар не будет добавлен в json-файл')

    print('-----------------------------')


def get_products_data_Shop_mts(link_products, driver, user_id):
    print(f'Ссылка на товар:{link_products}')

    def get_product_article(driver):
        try:
            article_element = driver.find_element(
                By.XPATH,
                "//span[contains(text(), 'Артикул: ')]"
            )

            article = article_element.text.split(': ')[1]
            return article

        except Exception as e:
            print(f"Ошибка при поиске артикула: {str(e)}")
            return None


    def get_product_title(driver):
        try:
            title_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//h2"))
            )

            title = title_element.text.strip()
            return title

        except Exception as e:
            print(f"Не удалось найти название товара: {str(e)}")
            return None


    def get_product_price(driver):
        try:
            out_of_stock = driver.find_element(By.CLASS_NAME, 'out-of-stock-block__text')

            return "Товара нет в наличии"

        except:
            try:

                price_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//span[contains(., '₽') and contains(., ' ')]")
                    )
                )

                price_text = price_element.text

                match = re.search(r'([\d\s]+)\s*₽', price_text)
                if match:
                    price = match.group(1).replace('\xa0', '').replace(' ', '').strip()
                    return price

            except Exception as e:
                print(f"Ошибка при получении цены: {str(e)}")
                return None


    def get_product_rating_reviews(driver):
        try:
            rating_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "span[class*='assessment'][class*='text']")
                )
            )
            rating = rating_element.text.replace(',', '.')

            assessment_block = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(@class, 'assessment-product__comments')]"))
            )

            review_count_element = assessment_block.find_element(By.XPATH, ".//span[contains(@class, 'assessment-product__text')]")

            reviews = review_count_element.text.strip()

            if rating == "Без оценки" or reviews == "0":
                return None, None
            else:
                return rating, reviews

        except Exception as e:
            print(f"Ошибка при получении рейтинга или отзывов: {e}")
            return None, None


    def get_product_images(driver):
        try:
            gallery_items = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[class*="product-gallery-preview__item"]'))
            )

            image_urls = []
            for item in gallery_items:
                img = item.find_element(By.CSS_SELECTOR, 'img.product-gallery-item__preview-image')
                url = img.get_attribute('data-src') or img.get_attribute('src')
                if url:
                    # Убираем параметр изменения размера из URL
                    original_url = url.split('/resize')[0]
                    image_urls.append(original_url)

            return image_urls

        except Exception as e:
            print(f"Ошибка при получении изображений: {str(e)}")
            return []


    article = get_product_article(driver)
    title = get_product_title(driver)
    price = get_product_price(driver)
    rating, reviews = get_product_rating_reviews(driver)
    image_urls = get_product_images(driver)

    # print(f'Артикул: {article}')
    # print(f'Заголовок товара: {title}')
    # print(f'Цена товара: {price}')
    # print(f'Рейтинг: {rating}')
    # print(f'Отзывы: {reviews}')
    # print(f"Найдено изображений: {len(image_urls)}")
    # for i in range(len(image_urls)):
    #     print(f'{i + 1}: {image_urls[i]}')


    if price == "Товара нет в наличии":
        print(f'Этот товар не будет добавлен: {price}')
    else:
        if article and title and price and rating and reviews:
            print(f'Артикул: {article}')
            print(f'Заголовок товара: {title}')
            print(f'Цена товара: {price}')
            print(f'Рейтинг: {rating}')
            print(f'Отзывы: {reviews}')
            print(f"Найдено изображений: {len(image_urls)}")

            for i in range(len(image_urls)):
                print(f'{i + 1}: {image_urls[i]}')

            Storing_data_Shop_mts(link_products, article, title, price, rating, reviews, image_urls, user_id)
        else:
            print(f'Этот товар не будет добавлен в json-файл')

    print('-----------------------------')



