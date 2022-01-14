# 저수율 데이터 객체
# data = AOI 작업 일
# group = 기종 그룹
# device = 기종 이름
# lot = Lot NO
# waferId = wafer id
# yield_ = 수율

# 자바빈 형식 (기본생성자, getter / setter)

class Loser():
    def __init__(self):
        self.date = None
        self.group = None
        self.device = None
        self.lot = None
        self.waferId = None
        self.yield_ = None

    def setDate(self, date):
        self.date = date

    def setGroup(self, group):
        self.group = group

    def setDevice(self, device):
        self.device = device

    def setWaferId(self, waferId):
        self.waferId = waferId

    def setYield(self, yield_):
        self.yield_ = yield_

    def setLot(self, lot):
        self.lot = lot

    def getDate(self):
        return self.date

    def getGroup(self):
        return self.group

    def getDevice(self):
        return self.device

    def getLot(self):
        return self.lot

    def getWaferId(self):
        return self.waferId

    def getYield_(self):
        return self.yield_