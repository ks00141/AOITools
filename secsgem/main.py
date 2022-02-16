import secsgem
import pymysql
import re


class TestEq(secsgem.GemEquipmentHandler):
    def __init__(self, address, port, active, session_id, name, custom_connection_handler=None):
        secsgem.GemEquipmentHandler.__init__(self, address, port, active, session_id, name, custom_connection_handler)
        self.con = pymysql.connect(user='root',
                                   password='wisol123',
                                   host='localhost',
                                   database='recipe',)
        self.cur = self.con.cursor()
        self.sql = ""

    def _on_s01f13(self, handler, packet):
        return secsgem.SecsS01F14({"COMMACK": secsgem.COMMACK.ACCEPTED, "MDLN": ["ARMS", "0.1.0"]})

    def _on_s02f41(self, handler, packet):

        data = self.secs_decode(packet)

        rcmd = data["RCMD"].get()
        params = data["PARAMS"].get()
        if rcmd == 'RECIPE_CHECK':

            cluster_recipe = params[0]["CPVAL"]
            frontside_recipe = params[1]["CPVAL"]
            cluster_recipe = re.sub('[\\\\]', '/', cluster_recipe)
            frontside_recipe = re.sub('[\\\\]', '/', frontside_recipe)

            try:
                self.sql_result = self.select_sql(select_columns='frontside_recipe',
                                                  from_table='spec',
                                                  find_column='cluster_recipe',
                                                  find_value=cluster_recipe)[0]
            except pymysql.err.ProgrammingError as e:
                code, msg = e.args
                print(code, msg)

            if self.sql_result == frontside_recipe:
                return secsgem.SecsS02F42({"HCACK": 0}), secsgem.SecsS06F11({"DATAID": 1,
                                                                             "CEID": 5686,
                                                                             "RPT": [
                                                                                 {
                                                                                     "RPTID": 1,
                                                                                     "V": "Recipe Info",
                                                                                     secsgem.SecsVarArray()
                                                                                 }
                                                                             ]})
            else:
                secsgem.SecsS02F42({"HCACK": 6})

        else:
            secsgem.SecsS02F42({"HCACK": 1})

    def select_sql(self, from_table, find_column, find_value, select_columns='*'):
        self.sql = 'SELECT `{}`'\
                   'FROM {} ' \
                   'WHERE `{}` = "{}"'\
                   .format(select_columns, from_table, find_column, find_value)
        self.cur.execute(self.sql)
        return self.cur.fetchone()


test_eq = TestEq(address='127.0.0.1',
                 port=1111,
                 active=False,
                 session_id=1,
                 name='test_eq')
test_eq.enable()
