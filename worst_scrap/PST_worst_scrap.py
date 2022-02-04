import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from login import login


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
time.sleep(5)
driver.get('https://outlook.office365.com')
login(id_='w2200810@wisol.co.kr',
      id_selector='#i0116',
      pwd_='daeduck!1',
      pwd_selector='#i0118',
      driver=driver)

