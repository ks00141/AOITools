# Loser 객체 Data Access Object
# 삭제 및 업데이트, 조회는 할일이 없어 Create만 구현
# DB Connection 정보
# host : localhost
# db : aoi
# port : 3306
# user : root
# passwd : wisol123

import pymysql


class LoserDao(object):

    def __init__(self):
        self.host = 'localhost'
        self.db = 'aoi'
        self.port = 3306
        self.user = 'root'
        self.password = 'wisol123'

    def insert(self, loser):
        conn = pymysql.connect(host=self.host,
                               user=self.user,
                               password=self.password,
                               port=self.port,
                               db=self.db)

        cur = conn.cursor()
        cur.execute('''INSERT INTO loser VALUES("{}","{}","{}","{}","{}","{}");'''.format(loser.getDate(),
                                                                                          loser.getGroup(),
                                                                                          loser.getDevice(),
                                                                                          loser.getLot(),
                                                                                          loser.getWaferId(),
                                                                                          loser.getYield_()))

        conn.commit()
        cur.close()
        conn.close()
