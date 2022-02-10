import pymysql
import datetime

start_date = (datetime.datetime.today() + datetime.timedelta(days=-1)).strftime('%Y-%m-%d 07:32:00')
end_date = datetime.datetime.today().strftime('%Y-%m-%d 07:32:00')
conn = pymysql.connect(host='10.20.10.101',
                       user='ymsview',
                       password='view.yms',
                       db='YMS')

cur = conn.cursor()
sql =   'SELECT ' \
        '* ' \
        'FROM ' \
        'YMS.ct_pst_vidata ' \
        'WHERE ' \
        f'`EVENTTIME` BETWEEN "{start_date}" ' \
        'AND ' \
        f'"{end_date}" ' \
        'AND ' \
        '`BIN00` / `BINTOTAL` * 100 < 98.1'

cur.execute(sql)
field_name = [i[0] for i in cur.description]
rows = cur.fetchall()

for row in rows:
    data = {head: data for head, data in zip(field_name, row)}
    print(data)

print(len(rows))