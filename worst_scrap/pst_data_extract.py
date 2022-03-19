import pymysql
import csv

f = open('pst_2022-02.csv', 'w', newline='', encoding='utf-8')
wr = csv.writer(f)

conn = pymysql.connect(user='ymsview',
                       password='view.yms',
                       host='10.20.10.101',
                       database='yms',
                       port=3306)
cur = conn.cursor()
sql = 'SELECT * FROM YMS.ct_pst_vidata WHERE `EVENTTIME` BETWEEN "2022-02-01" AND "2022-03-01"'
cur.execute(sql)
data = cur.fetchall()
field_name = [i[0] for i in cur.description]
wr.writerow(field_name)
wr.writerows(data)
f.close()



