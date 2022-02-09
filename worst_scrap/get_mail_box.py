import time

def get_mail_box(by, driver):
    # driver.find_element(by.CSS_SELECTOR,
    #                     '#app > '
    #                     'div > '
    #                     'div.zZJcFiYp1GsQ-Zkcz02eC >'
    #                     'div.mXEfuMleN9V2Rx6d6qvsu >'
    #                     'div._2aSECY2_aC8BM-pa12gLyl >'
    #                     ' div > '
    #                     'div > '
    #                     'div.tQjtZGBXoedSUDzkcRzw5 >'
    #                     ' div._1mmhFz6xbEHFv6FfTUKPW2 > '
    #                     'div >'
    #                     ' div >'
    #                     ' div >'
    #                     ' div:nth-child(4) >'
    #                     ' div:nth-child(9) >'
    #                     ' div').click()
    btns = driver.find_elements(by.CLASS_NAME,
                                'ms-Button')

    for btn in btns:
        if btn.get_attribute("title") == '왼쪽 창 전환':
            btn.click()
            break

    time.sleep(5)
    divs = driver.find_elements(by.XPATH,
                                 '//div[@title]')

    for div in divs:
        if div.get_attribute("title") == 'worstYield':
            div.click()
            break
