from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from login import login
from get_mail_box import get_mail_box
from input_key import input_key
import time
from datetime import datetime
from return_titles import return_titles
from kafka_producer import kafka_producer
import json
from kafka import KafkaProducer


TIMEDELAY = 5   # Web Browser Lading Delay
TODAY = datetime.today().date().strftime('[%Y-%m-%d]')  # 메일 제목 오늘 날짜 설정
FINDTITLE = '[CSP,WLP]최종외검 저수율 리스트 ' + TODAY  # 찾을 메일 제목
TITLECLASSNAME = 'NsB53xFTU532cgP0ztFSC'    # 메일 제목 HTML class attr value

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))     # Selenium Chrome Browser 실행

time.sleep(TIMEDELAY)       # Browser 로딩 시간 대기
driver.get('https://outlook.office365.com')     # outlook page 접속

# login method
login(id_='w2200810@wisol.co.kr',       # outlook id
      id_selector='#i0116',             # outlook page id 입력창 HTML id attr value
      pwd_='daeduck!1',                 # outlook pwd
      pwd_selector='#i0118',            # outlook page pwd 입력창 id attr value
      driver=driver,                    # webdriver class
      by=By,                            # element 탐색을 위한 webdriver.common.by.By class
      time=time,                        # input_key method delay 를 위한 time class
      keys=Keys,                        # enter 입력을 위한 webdriver.common.keys.Keys class
      input_key=input_key)              # input_key method 전달

time.sleep(TIMEDELAY)       # Browser 로딩 시간 대기

# worst mailbox click method
get_mail_box(by=By,             # element 탐색을 위한 webdriver.common.by.By class
             driver=driver)     # webdriver class

time.sleep(TIMEDELAY)       # Browser 로딩 시간 대기

# worst mailbox 에서 mail titles 획득
elems = return_titles(driver=driver,                # webdriver class
                      by=By,                        # webdriver.common.by.By class
                      class_name=TITLECLASSNAME)    # 메일 제목 class attr value

# mail list 에서 target mail 찾기
for elem in elems:                                                                  # mail list 탐색
    title = elem.get_attribute('aria-label')                                        # mail element aria-label attr = 메일 제목
    print(title)
    if FINDTITLE in title:                                                          # 메일 제목 에서 찾고자 하는 메일 제목 문자열이 있는지
        elem.click()                                                                # 해당하는 메일 mail click
        time.sleep(TIMEDELAY)                                                       # 메일 로딩 대기
        table = driver.find_element(By.XPATH, '//*[@id="x_summary"]/tbody')         # 메일 내용에서 table element 선택
        th = table.find_elements(By.TAG_NAME, 'th')                                 # table element에서 table header 추출
        for tr in table.find_elements(By.TAG_NAME, 'tr')[1:]:                       # table 첫번째 행 제외하고 반복문 실행
            td = tr.find_elements(By.TAG_NAME, 'td')                                # table desc 획득
            data = {head.text:value.text for head, value in zip(th, td)}            # key = th, value = td dict 생성
            data_json = json.dumps(data,                                            # data dict -> data json 변환
                                   ensure_ascii=False)                              # 한글 저장을 위해 ascii encoding X

            print(data_json)                                                        # json console 출력
            kafka_producer(producer=KafkaProducer,                                  # kafka 전송
                           data=data_json,
                           server_ip='localhost:9092',
                           topic='NS')
        break

