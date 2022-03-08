import secsgem
import pymysql
import re


class TestEq(secsgem.GemEquipmentHandler):
    def __init__(self, address, port, active, session_id, name, custom_connection_handler=None):
        secsgem.GemEquipmentHandler.__init__(self, address, port, active, session_id, name, custom_connection_handler)
        # self.con = pymysql.connect(user='root',
        #                            password='wisol123',
        #                            host='localhost',
        #                            database='recipe',)
        # self.cur = self.con.cursor()
        # self.sql = ""

    def _on_s01f13(self, handler, packet):
        return secsgem.SecsS01F14({"COMMACK": secsgem.COMMACK.ACCEPTED, "MDLN": ["ARMS", "0.1.0"]})

    def _on_s02f41V3(self, handler, packet):
        print(self.data_values)
        return secsgem.SecsS02F42({"HCACK": 0})

    # def select_sql(self, from_table, find_column, find_value, select_columns='*'):
    #     self.sql = 'SELECT `{}`'\
    #                'FROM {} ' \
    #                'WHERE `{}` = "{}"'\
    #                .format(select_columns, from_table, find_column, find_value)
    #     self.cur.execute(self.sql)
    #     return self.cur.fetchone()
    #

test_eq = TestEq(address='127.0.0.1',
                 port=1111,
                 active=False,
                 session_id=1,
                 name='test_eq')
test_eq.enable()
