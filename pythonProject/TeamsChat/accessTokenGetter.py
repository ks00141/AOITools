from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get("https://developer.microsoft.com/en-us/graph/graph-explorer")
time.sleep(3)
login_btn = driver.find_element(By.XPATH, '//button[@aria-label="Sign in to Graph Explorer"]')
original_window = driver.window_handles[0]
print(original_window)
webdriver.ActionChains(driver).click(login_btn).perform()
time.sleep(3)
driver.switch_to.window(driver.window_handles[-1])
print(driver.current_window_handle)
id_input = driver.find_element(By.XPATH, '//input[@name="loginfmt"]')
id_input.send_keys('w2200810@wisol.co.kr')
time.sleep(1)
id_input.send_keys(Keys.ENTER)
time.sleep(3)
pwd_input = driver.find_element(By.XPATH, '//input[@name="passwd"]')
pwd_input.send_keys('K8s,Docker')
time.sleep(1)
pwd_input.send_keys(Keys.ENTER)
time.sleep(3)
back_btn = driver.find_element(By.XPATH, '//input[@id="idBtn_Back"]')
webdriver.ActionChains(driver).click(back_btn).perform()
time.sleep(3)
driver.switch_to.window(original_window)
time.sleep(3)
