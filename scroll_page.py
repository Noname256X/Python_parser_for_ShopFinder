import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

def dynamic_scroll(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")

    actions = ActionChains(driver)

    while True:
        for i in range(5):
            actions.send_keys(Keys.PAGE_DOWN).perform()

        time.sleep(1)

        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break

        last_height = new_height
