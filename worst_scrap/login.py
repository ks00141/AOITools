def login(id_, id_selector, pwd_, pwd_selector, by, driver, keys, time, input_key, delay=5, login_option=True):
    time.sleep(delay)
    input_key(elem=driver.find_element(by.CSS_SELECTOR, id_selector),
              key=id_,
              keys=keys,
              time=time)
    time.sleep(delay)
    input_key(elem=driver.find_element(by.CSS_SELECTOR, pwd_selector),
              key=pwd_,
              keys=keys,
              time=time)
    time.sleep(delay)
    if login_option:
        driver.find_element(by.CSS_SELECTOR, '#idBtn_Back').click()
