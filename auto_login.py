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
    browser.add_cookie({"name": "MUSIC_U", "value": "000DE287D57324A621FD8C0A08B70E0A05F58CF9CB756E0BC3F62ED1C4122E60879CED2CFA92EC28B96F64ED323F7BFFE17129E0D4ED3236DE13032BC1ED1A47708854C1C5CE8D8C5FDEFE3B7BEAA780A1A838EF1BF159401C147B18A23695FCF34EB77154CC69FA79A7236CA85E5C12DA5CDDD198CBC7CE0D7040DFBEA8AA91133AAC8C3631CE821FA4900B2946C7EAFFCDF541C3B4F0A31872A87FDBB4E8A0678C2337A7177A4F71E192E9004A1FE9A1A9A5E5361ECE5632548EE2CA86F7A6D960FCC96BF066879C0DB2E912308FE4FCDAEF21CF5B87FB86D6D7EBC4DFE8BF6879CC97E13032B3612295A73BF7FE28184A85D6CB540A32CA3D0B24D1A8C263E026C8D61F34E91FD032A8DE5A1F64965D5E4F1B33BE083FB585668530D265829CCFE24E3C4F71538C79390A3DFFB4E20C864F4B0B3EB8B6286D5ED8CA27498B3D8B5771CA99F1E690C88EF4BEC80CABE0"})
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
