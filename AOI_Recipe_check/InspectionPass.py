'''
 // 211209
  - Model Instance 생성시 Model의 inspection_passes에 저장되는 
    Inspection pass별로 설정값 class
  - instance 생성시 멤버 변수 찾을수가 없다고 에러가 뜸 왜지..

 // 211211
  - 멤버변수의 초기값이 없어서 멤버 변수를 찾을수 없다고 뜸
    아마 Python 특성상 자료형의 구분이 없기때문에? 이게 변수인지 다른 호출자의 이름인지
    구분을 하지 못해서 발생하는듯 앞으로 멤버변수의 초기값은 None으로 직접 주자
'''

class InspectionPass():
    def __init__(self):
        self.magnification = None
        self.illumination = None
        self.inspection_options = []