import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time


def Checking_Avito(city, user_id):
    driver = uc.Chrome(version_main=135)
    driver.implicitly_wait(10)

    try:
        driver.get('https://www.avito.ru')
        time.sleep(3)

        location_span = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, "//span[contains(@class, 'buyer-pages-mfe-location-nev1ty') and text()='Ростов-на-Дону']")
            )
        )

        driver.execute_script("arguments[0].click();", location_span)
        time.sleep(5)


    finally:
        driver.quit()
        print('-----------------------------')


# def Checking_Youla(city, user_id):
#     driver = uc.Chrome(version_main=135)
#     driver.implicitly_wait(10)
#
#     try:
#         driver.get('https://www.avito.ru')
#         time.sleep(3)
#
#
#     finally:
#         driver.quit()
#         print('-----------------------------')







Checking_Avito(city='Самара', user_id='12331224')








