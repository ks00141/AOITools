import time
from selenium.webdriver.common.keys import Keys


def input_key(elem, key, option='ENTER', delay=5):
    elem.send_keys(key)
    if option == 'ENTER':
        time.sleep(delay)
        elem.send_keys(Keys.ENTER)
