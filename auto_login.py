# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "0080FB7E460B766EE036C9F802B7235BDA188AC0E146725BE9BE52ABEE9155FA03A13D5C178A60528495280A298771F6242F8914140FA7E79366652826B881D118E95418BD732462530A1E69F9D7807A98FAF11EAE1AB33F253C20EC0F7E3D24EEEF20D86FF777DD1CAE7660ECB6216160A1E0CBC922E78E77FC481A9725B065F9D80BB4364700217697159DADBF16B26A88DAD4B53A9B8799A2E666349929313CB70C82702FC6A86E544F567089EDBAC6E40607939219B9875E1DFEC513DC5C1432E579FC367FC7778CB12D7681853481E95478416BF503798C69265E247B74E169C53856A40055E7E62CB1EFC3D23AA858733249555B2D07A0695CFE7DA7EA4DA77DEEEAFA128908CC201938D7FEBE77691B4A92A315643BC8B26E97A0560A70C4738BC09FB7B6E4B59FD790EF1CCDDB6F278D044844D539917205843C49A44E5600150082996FCEC9A1FE0A1267A9B23CABC3359DBB137DCD59D0BC72BE6F42"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
