from dao.LoserDao import LoserDao
from object.Loser import Loser
import re
import os
import pandas as pd
import shutil
import configparser
import datetime

# Configparser load , root path set
c = configparser.ConfigParser()
c.read('./config.ini')
root = c['path']['root']

# worst yield wafer = loser
# loser object, loser data access object instance
loser = Loser()
loserDao = LoserDao()

# 파일명 규칙 : (DB저장 유무)_(그룹)_저수율list_([저장일자]).xlsx
# 월단위 저장 폴더명 규칙 : (yymm)
# Dir structure
# root
# ├──zzbackup // 전년도 백업용 폴더
# ├──TC       // FINAL AOI TC 기종 (TC-CSP, TC-WLP)
# │   └─(yymm)... //월별 저수율 리스트 폴더
# │      └─(DB저장 유무)_(그룹)_저수율list_([저장일자]).xlsx //일별 저수율 리스트 xlsx 파일
# ├──PST      // PST AOI 저수율
# │   └─(yymm)... //월별 저수율 리스트 폴더
# │      └─(DB저장 유무)_(그룹)_저수율list_([저장일자]).xlsx //일별 저수율 리스트 xlsx 파일
# ├──NS       // FINAL AOI NS 기종 (Normal CSP, Normal WLP)
# │   └─(yymm)... //월별 저수율 리스트 폴더
# │      └─(DB저장 유무)_(그룹)_저수율list_([저장일자]).xlsx //일별 저수율 리스트 xlsx 파일

month = datetime.datetime.today().strftime("%y%m")
# zzbackup 폴더를 제외한 그룹별 저수율 데이터 폴더 순회
for group in os.listdir(root)[:-1]:

    # 일별 저수율 데이터 파일 순회
    for file in os.listdir(os.path.join(root, group, month)):
        # 파일 이름 맨 앞글자가 C가 아니면 DB에 저장
        if 'C' not in file[0]:

            # 파일명에서 날짜 추출
            date = re.search('([0-9]+)-([0-9]+)-([0-9]+)', file.split('_')[-1]).group()
            # 파일명에서 그룹명 추출
            group = file.split("_")[0]
            # xlsx 파일 판다스로 열기
            data = pd.read_excel(os.path.join(root, group, month, file), engine='openpyxl').drop('NO', axis=1,)
            # 데이터 행단위 순회
            for row in data.values:

                loser.setDate(date)
                loser.setGroup(group)
                loser.setDevice(row[0])     # 첫번째 열 = 기종명
                loser.setLot(row[1])        # 두번째 열 = Lot no
                loser.setWaferId(row[2])    # 세번째 열 = wafer id
                loser.setYield(row[3])      # 네번째 열 = 수율

                # DB insert
                try:
                    loserDao.insert(loser)
                    print('''
== 입력 완료== 
{}_{}_{}_{}_{}'''.format(loser.getGroup(), loser.getDate(), loser.getDevice(), loser.getLot(), loser.getWaferId()))

                # Exception 발생시 중복데이터로 간주 예외처리
                except Exception:
                    print('''
!! 중복된 데이터 입니다
{}_{}_{}_{}_{}'''.format(loser.getGroup(), loser.getDate(), loser.getDevice(), loser.getLot(), loser.getWaferId()))

            # DB 저장 완료 파일은 파일명 변경 (맨앞에 'C_' 라고 표시)
            shutil.move(os.path.join(root, group, month, file), os.path.join(root, group, month, ('C_' + file),))





