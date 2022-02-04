from selenium import webdriver
from selenium.webdriver.common.by import By
from input_key import input_key
import time


def login(id_, id_selector, pwd_, pwd_selector, driver, delay=5, login_option=True):
    time.sleep(delay)
    input_key(elem=driver.find_element(By.CSS_SELECTOR, id_selector),
              key=id_)
    time.sleep(delay)
    input_key(elem=driver.find_element(By.CSS_SELECTOR, pwd_selector),
              key=pwd_)
    time.sleep(delay)
    if login_option:
        driver.find_element(By.CSS_SELECTOR, '#idBtn_Back').click()
