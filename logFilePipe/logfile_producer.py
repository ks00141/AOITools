import os
import json
import re
import xml.etree.ElementTree as elemTree
from kafka import KafkaProducer

# config.json 설정 파일로 부터 log file 이 수집된 경로 설정
# lograwpath : log file path
with open('config.json', encoding='utf-8') as f:
    config = json.load(f)
    log_root = config['logrootpath']

# log file root dir
#  └─주차별 log 파일 (?W ~ ??W)
#      ├─ 설비별 log 파일 (#9,#10,#11,#12)
#      └─ 일별 lop 파일 (? ~ ??)
#           └─ logfile.xml

# log root 하위에 test 폴더나, class 폴더가 섞여있음
# class폴더 : 주차별 폴더 생성시 편의를 위해 미리 #9~#12 라는 폴더가 생성된 폴더
# 정규식을 이용해서 1~2자리 숫자 + W 라는 이름의 폴더만 선택하기
# [0-9]{1,2}W
# file_list : log root 하위 모든 폴더
# files : 정규식으로 한번 걸러낸 폴더 (log folder)
p = re.compile('[0-9]{1,2}W')
file_list = os.listdir(log_root)
files = [file for file in file_list if p.match(file)]

# 순서
# 1. Json으로 변환시킬 Dict obj 생성
# 2. XML 파일 읽기
# 3. Dict 대입
# 4. dict -> Json으로 변환
# 5. Json 전송

# kafka producer 생성
producer = KafkaProducer(acks=0,
                         bootstrap_servers=['localhost:9092'])


# 파일 접근
# 순서대로 접근하고 merge 완료된 파일은 완료 flag 를 넣어둔다 (ex : 맨앞에 'C_')
count = 0
for week in files:
    for tool in os.listdir(os.path.join(log_root, week)):
        for day in os.listdir(os.path.join(log_root, week, tool)):
            # Dict obj 생성
            log_dict = dict()
            for file in os.listdir(os.path.join(log_root, week, tool, day)):
                # xml 파일 읽기
                root = elemTree.parse(source=os.path.join(log_root, week, tool, day, file)).getroot()
                # root node의 자식노드가 0개 보다 많으면
                if len(root) > 0:
                    # child node tag : child node value dict 생성, dict obj 대입
                    log_dict = {leaf_1.tag: leaf_1.text for leaf_1 in root}
                    # 설비 번호 추가
                    log_dict['tool'] = tool
                    print(log_dict)
                    # dict obj json 으로 변환
                    log_json = json.dumps(log_dict,
                                          ensure_ascii=False).encode('utf-8')
                    producer.send(topic='datastudy',
                                  value=log_json)

print(count)
