import pymysql

conn = pymysql.connect(host = '127.0.0.1', user = 'root', passwd = 'wisol123', db = 'recipe', port = 3306, charset="utf8")
cur = conn.cursor()

cur.execute('select * from spec where DEVICE = "SX897FYTTF02";')

cur.fetchall()

conn.close()