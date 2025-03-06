import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import json


def get_products_links_Ozon(item_name):
    driver = uc.Chrome(version_main=133)
    driver.implicitly_wait(10)

    try:
        driver.get('https://ozon.ru')
        time.sleep(7)

        find_input = driver.find_element(By.NAME, 'text')
        find_input.clear()
        find_input.send_keys(item_name)
        time.sleep(2)
        find_input.send_keys(Keys.ENTER)
        time.sleep(2)

        try:
            find_links = driver.find_elements(By.CSS_SELECTOR, 'div.tile-root a.tile-clickable-element')
            product_urls = [link.get_attribute("href") for link in find_links if link.get_attribute("href") is not None]

        except Exception as e:
            print(f'[!] Что-то пошло не так при сборе ссылок на товары Ozon: {e}')

        product_urls_dict = {}

        for k, v in enumerate(product_urls):
            product_urls_dict.update({k: v})

        if product_urls:
            with open('links to json products/products_urls_ozon.json', 'w', encoding='utf-8') as file:
                json.dump(product_urls, file, indent=4, ensure_ascii=False)
            print(f'[+] Ссылки на товары Ozon сохранены в файл!')
        else:
            print('[!] Не удалось собрать ссылки на товары Ozon.')


    finally:
        driver.quit()


def get_products_links_WB(item_name):
    driver = uc.Chrome(version_main=133)
    driver.implicitly_wait(10)

    try:
        driver.get('https://www.wildberries.ru')
        time.sleep(5)

        find_input = driver.find_element(By.CSS_SELECTOR, '[data-wba-header-name="Search_text"]')
        find_input.clear()
        find_input.send_keys(item_name)
        time.sleep(2)
        find_input.send_keys(Keys.ENTER)
        time.sleep(2)

        try:
            find_links = driver.find_elements(By.CSS_SELECTOR, 'a.product-card__link')
            product_urls = [link.get_attribute("href") for link in find_links if link.get_attribute("href") is not None]

        except Exception as e:
            print(f'[!] Что-то пошло не так при сборе ссылок на товары WB: {e}')

        product_urls_dict = {}

        for k, v in enumerate(product_urls):
            product_urls_dict.update({k: v})

        if product_urls:
            with open('links to json products/products_urls_wb.json', 'w', encoding='utf-8') as file:
                json.dump(product_urls, file, indent=4, ensure_ascii=False)
            print(f'[+] Ссылки на товары WB сохранены в файл!')
        else:
            print('[!] Не удалось собрать ссылки на товары WB.')

    finally:
        driver.quit()


def get_products_links_YandexMarket(item_name):
    driver = uc.Chrome(version_main=133)
    driver.implicitly_wait(10)

    try:
        driver.get('https://market.yandex.ru')
        time.sleep(4)


        find_input = driver.find_element(By.NAME, 'text')
        find_input.clear()
        find_input.send_keys(item_name)
        time.sleep(2)
        find_input.send_keys(Keys.ENTER)
        time.sleep(2)

        try:
            find_links = driver.find_elements(By.CSS_SELECTOR, 'a.EQlfk')
            product_urls = {
                link.get_attribute("href") for link in find_links
                if link.get_attribute("href") is not None and "/product--" in link.get_attribute("href")
            }

        except Exception as e:
            print(f'[!] Что-то пошло не так при сборе ссылок на товары Я.Маркет: {e}')

        product_urls = list(product_urls)

        if product_urls:
            with open('links to json products/products_urls_yandex_market.json', 'w', encoding='utf-8') as file:
                json.dump(product_urls, file, indent=4, ensure_ascii=False)
            print(f'[+] Ссылки на товары Я.Маркет сохранены в файл!')
        else:
            print('[!] Не удалось собрать ссылки на товары Я.Маркет.')

    finally:
        driver.quit()


def get_products_links_MagnitMarket(item_name):
    driver = uc.Chrome(version_main=133)
    driver.implicitly_wait(10)

    try:
        driver.get('https://mm.ru')
        time.sleep(3)


        find_input = driver.find_element(By.CSS_SELECTOR, 'input.default-input')
        find_input.clear()
        find_input.send_keys(item_name)
        time.sleep(2)
        find_input.send_keys(Keys.ENTER)
        time.sleep(2)

        try:
            find_links = driver.find_elements(By.CSS_SELECTOR, 'div[data-test-id="item__product-card"] a[ui-link="ui-link"]')
            product_urls = [link.get_attribute("href") for link in find_links if link.get_attribute("href") is not None]

        except Exception as e:
            print(f'[!] Что-то пошло не так при сборе ссылок на товары М.Маркет: {e}')

        product_urls = list(product_urls)

        if product_urls:
            with open('links to json products/products_urls_magnit_market.json', 'w', encoding='utf-8') as file:
                json.dump(product_urls, file, indent=4, ensure_ascii=False)
            print(f'[+] Ссылки на товары М.Маркет сохранены в файл!')
        else:
            print('[!] Не удалось собрать ссылки на товары М.Маркет.')

    finally:
        driver.quit()


def get_products_links_DNS(item_name):
    driver = uc.Chrome(version_main=133)
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


def get_products_links_Citilink(item_name):
    driver = uc.Chrome(version_main=133)
    driver.implicitly_wait(10)

    try:
        driver.get('https://www.citilink.ru')
        time.sleep(3)

        find_input = driver.find_element(By.NAME, 'text')
        find_input.clear()
        find_input.send_keys(item_name)
        time.sleep(2)
        find_input.send_keys(Keys.ENTER)
        time.sleep(2)

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


# def Eldorado (captcha)


def get_products_links_M_Video(item_name):
    driver = uc.Chrome(version_main=133)
    driver.implicitly_wait(10)

    try:
        driver.get('https://www.mvideo.ru')
        time.sleep(3)

        find_input = driver.find_element(By.CSS_SELECTOR, 'input.input__field')
        find_input.clear()
        find_input.send_keys(item_name)
        time.sleep(2)
        find_input.send_keys(Keys.ENTER)
        time.sleep(2)

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







def main():
    #get_products_links_Ozon('наушники xiaomi')
    #get_products_links_WB('наушники xiaomi')
    #get_products_links_YandexMarket('наушники xiaomi')
    #get_products_links_MagnitMarket('наушники xiaomi')
    #get_products_links_DNS('наушники xiaomi')
    #get_products_links_Citilink('наушники xiaomi')
    #get_products_links_M_Video('наушники xiaomi')




if __name__ == '__main__':
    main()
