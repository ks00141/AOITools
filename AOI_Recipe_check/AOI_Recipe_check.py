'''
// 211207
 - ROI Viewer 기능 삭제 (ROI 획득 문제로 잠정 개발 중단)
 / from ImageLoader import ImageLoader /

// 211208
 - Parameters(SPEC, TOOL Setting, Check) View 추가 (listbox)
 - PST-AOI , FINAL Layer 구분 추가 (Radio Button)
 - ROI Viewer 자리에 Inspection Pass 정보 칸 삽입

// 211221
 - UI 배치 변경
 - IDT , IDT_SUB, PAD, Pin Mark
'''


import os
from tkinter import *
from tkinter import messagebox
from RecipeLoader import RecipeLoader


class Main():
    def __init__(self):
        self.window = Tk()
        self.flag = 'PST'

        # Recipe 항목별로 해당하는 Entry를 넣기 위한 Dict
        # 이름을 확인하고 넣으려고 Key값 확인이 가능한 Dict 형으로 선언
        # Value는 여러값이 있을수도 있어서 리스트 형으로 선언
        # 각 항목별로 해당하는 Entry를 담는다 
        self.inspection_option = {'tool' : {
                                    'magnification' : [],
                                    'illumination' : [],
                                    'idt' : [],
                                    'idt_sub' : [],
                                    'pad' : [],
                                    'pin_mark' : []},
                                  'spec' : {
                                    'magnification' : [],
                                    'illumination' : [],
                                    'idt' : [],
                                    'idt_sub' : [],
                                    'pad' : [],
                                    'pin_mark' : []}
                                  }
        self.window.title('AOI Recipe Check')

        # Spec, Tool value 비교를 위한 리스트
        # Sepc, Tool Entry가 해당하는 항목별로 순서대로 담김
        self.spec_entrys = []
        self.tool_entrys = []
        self.check_entrys = []

        # window size setting
        self.window.geometry('650x480')

        # Recipe Viwer Layer
        # Device 입력시 cluster(PPID), frontside Recipe 이름이 출력되는 entry

        # Viwer Layer Frame
        self.recipe_viwer_layer = Frame(self.window,
                                        width = 650,
                                        height = 110)
        self.recipe_viwer_layer.grid(row = 0,
                                     column = 0)


        

        # Labels (device / cluster / frontside)
       
        self.label_xpos = 30
        
        self.lbl_device = Label(self.recipe_viwer_layer,
                           text = 'Device',)
        self.lbl_device.place(x = self.label_xpos,
                              y = 20,)

        self.lbl_cluster = Label(self.recipe_viwer_layer,
                                 text = 'Cluster',)
        self.lbl_cluster.place(x = self.label_xpos,
                               y = 50,)

        self.lbl_frontside = Label(self.recipe_viwer_layer,
                                   text = 'Frontside',)
        self.lbl_frontside.place(x = self.label_xpos,
                                 y = 80,)

        
        # Entry (device / cluster / frontside)

        self.entry_width = 50
        self.entry_xpos = 100

        self.et_device = Entry(self.recipe_viwer_layer,
                               width = self.entry_width)
        self.et_device.place(x = self.entry_xpos,
                        y = 20,)

        self.et_cluster = Entry(self.recipe_viwer_layer,
                                width = self.entry_width)
        self.et_cluster.place(x = self.entry_xpos,
                              y = 50,)

        self.et_frontside = Entry(self.recipe_viwer_layer,
                                  width = self.entry_width)
        self.et_frontside.place(x = self.entry_xpos,
                                y = 80,)

        # AOI Layer Select Radio Button
        # PST AOi , FINAL AOI 두 Layer중 하나를 고르는 radio button

        self.radio_xpos = 470

        self.AOI_layer = StringVar()
        self.rb_pst = Radiobutton(self.recipe_viwer_layer,
                                  text = 'PST-AOI',
                                  value = 'PST',
                                  variable = self.AOI_layer,
                                  command = self.set_flag)
        self.rb_pst.select()
        self.rb_pst.place(x = self.radio_xpos,
                          y = 28)

        self.rb_final = Radiobutton(self.recipe_viwer_layer,
                                    text = 'FINAL',
                                    value = 'FINAL',
                                    variable = self.AOI_layer,
                                    command = self.set_flag)
        self.rb_final.place(x = self.radio_xpos,
                            y = 60)


        # Load Button
        # Device Entry에 입력된 내용을 가지고 정보를 불러오는 여러 메소드 트리거 버튼

        self.load_btn_xpos = 550
        self.export_button_width = 10
        self.export_button_height = 5

        self.btn_export = Button(self.recipe_viwer_layer,
                                 text = 'Load',
                                 width = self.export_button_width,
                                 height = self.export_button_height,
                                 command = self.load,)
        self.btn_export.place(x = self.load_btn_xpos,
                              y = 18)
        
        # Settings Layer
        # cluster(PPID), frontside recipe 외에 inspection parameter 정보가 나타나는 영역

        self.spec_ets_pos_x = 200
        self.tool_ets_pos_x = 320
        self.check_ets_pos_x = 440

        # Settings Layer Frame
        self.settings_layer = LabelFrame(self.window,
                                    relief='solid',
                                    text = 'Settings',
                                    bd =1,
                                    width = 550,
                                    height = 300)
        self.settings_layer.grid(row = 1,
                                 column = 0,
                                 padx = 10,
                                 pady = 20,)

        
        # Number Of Inspection Pass
        # 해당 recipe의 inspection pass가 몇개인지 표시(1pass , 2pass)
        self.lbl_noip = Label(self.settings_layer,
                              text = 'Inspection Pass')
        self.lbl_noip.place(x = 50,
                            y = 40)

        # Spec Value (NOIP)
        # inspection pass 갯수의 spec
        self.et_noip_spec = Entry(self.settings_layer,
                             width = 5,)
        self.et_noip_spec.place(x = self.spec_ets_pos_x,
                                y = 40)
        self.spec_entrys.append(self.et_noip_spec)

        
        # Tool Value (NOIP)
        # 실제 reciep에 셋업된 inspection pass
        self.et_noip_tool = Entry(self.settings_layer,
                             width = 5,)
        self.et_noip_tool.place(x = self.tool_ets_pos_x,
                                y = 40)
        self.tool_entrys.append(self.et_noip_tool)

        # inspection magnification / illumination
        # 조명밝기, 배율 정보가 나타나는 영역
        # Magnification
        Label(self.settings_layer,
              text = '검사 배율').place(x = 50,
                                            y = 80)

        # 1Pass
        self.lbl_1pass_magnification = Label(self.settings_layer,
                                             text = '1PASS')
        self.lbl_1pass_magnification.place(x = 150,
                                           y = 80)

        # Spec Value (Magnification 1PASS)
        # recipe 첫번째 pass의 검사 배율 spec
        self.et_1pass_spec_magnification = Entry(self.settings_layer,
                                            width = 5)
        self.et_1pass_spec_magnification.place(x = self.spec_ets_pos_x,
                                          y = 80)

        self.inspection_option['spec']['magnification'].append(self.et_1pass_spec_magnification)
        self.spec_entrys.append(self.et_1pass_spec_magnification)

        # Tool Value (Magnification 1PASS)
        # recipe 첫번째 pass 의 실제 셋팅된 검사 배율
        self.et_1pass_tool_magnification = Entry(self.settings_layer,
                                            width = 5)
        self.et_1pass_tool_magnification.place(x = self.tool_ets_pos_x,
                                          y = 80)

        self.inspection_option['tool']['magnification'].append(self.et_1pass_tool_magnification)
        self.tool_entrys.append(self.et_1pass_tool_magnification)

        # 2Pass
        self.lbl_2pass_magnification = Label(self.settings_layer,
                                             text = '2PASS')
        self.lbl_2pass_magnification.place(x = 150,
                                           y = 100)

        # Spec Value (Magnification 2PASS)
        # recipe 두번째 pass의 검사 배율 spec
        self.et_2pass_spec_magnification = Entry(self.settings_layer,
                                            width = 5)
        self.et_2pass_spec_magnification.place(x = self.spec_ets_pos_x,
                                               y = 100)

        self.inspection_option['spec']['magnification'].append(self.et_2pass_spec_magnification)
        self.spec_entrys.append(self.et_2pass_spec_magnification)

        # Tool Value (Magnification 2PASS)
        # recipe 두번째 pass 실제 셋팅된 검사 배율
        self.et_2pass_tool_magnification = Entry(self.settings_layer,
                                                 width = 5)
        self.et_2pass_tool_magnification.place(x = self.tool_ets_pos_x,
                                               y = 100)
        
        self.inspection_option['tool']['magnification'].append(self.et_2pass_tool_magnification)
        self.tool_entrys.append(self.et_2pass_tool_magnification)

        # Illumination
        Label(self.settings_layer,
              text= '조명 밝기').place(x = 50,
                                      y = 130)
        
        # 1PASS
        self.lbl_1pass_illumination = Label(self.settings_layer,
                                            text = '1PASS')
        self.lbl_1pass_illumination.place(x = 150,
                                          y = 130)

        # Spec Value (Illumination 1PASS)
        # recipe 첫번째 pass의 검사 밝기 spec
        self.et_1pass_spec_illumination = Entry(self.settings_layer,
                                           width = 5)
        self.et_1pass_spec_illumination.place(x = self.spec_ets_pos_x,
                                         y = 130)
        self.inspection_option['spec']['illumination'].append(self.et_1pass_spec_illumination)
        self.spec_entrys.append(self.et_1pass_spec_illumination)

        # Tool Value (Magnification 1PASS)
        # recipe 첫번째 pass의 실제 셋팅된 검사 밝기
        self.et_1pass_tool_illumination = Entry(self.settings_layer,
                                           width = 5)
        self.et_1pass_tool_illumination.place(x = self.tool_ets_pos_x,
                                         y = 130)
        self.inspection_option['tool']['illumination'].append(self.et_1pass_tool_illumination)
        self.tool_entrys.append(self.et_1pass_tool_illumination)

        # 2PASS
        self.lbl_2pass_illumination = Label(self.settings_layer,
                                            text = '2PASS')
        self.lbl_2pass_illumination.place(x = 150,
                                          y = 150)

        # Spec Value (Illumination 2PASS)
        # recipe 두번째 pass의 검사 밝기 spec
        self.et_2pass_spec_illumination = Entry(self.settings_layer,
                                           width = 5)
        self.et_2pass_spec_illumination.place(x = self.spec_ets_pos_x,
                                         y = 150)
        self.inspection_option['spec']['illumination'].append(self.et_2pass_spec_illumination)
        self.spec_entrys.append(self.et_2pass_spec_illumination)

        # Tool Value (Magnification 2PASS)
        # reicpe 두번째 pass의 실제 셋팅된 검사 밝기
        self.et_2pass_tool_illumination = Entry(self.settings_layer,
                                           width = 5)
        self.et_2pass_tool_illumination.place(x = self.tool_ets_pos_x,
                                         y = 150)
        self.inspection_option['tool']['illumination'].append(self.et_2pass_tool_illumination)
        self.tool_entrys.append(self.et_2pass_tool_illumination)

        # IDT
        # IDT : 1pass
        # IDB_SUB : 2pass
        self.lbl_idt = Label(self.settings_layer,
                             text = 'IDT')
        self.lbl_idt.place(x = 50,
                           y = 170)

        # Spec Value (IDT)
        # recipe IDT 검사 spec
        self.et_spec_idt = Entry(self.settings_layer,
                                 width = 5)
        self.et_spec_idt.place(x = self.spec_ets_pos_x,
                               y = 170)
        self.inspection_option['spec']['idt'].append(self.et_spec_idt)
        self.spec_entrys.append(self.et_spec_idt)

        # Tool Value (IDT)
        # recipe IDT 검사 실제 셋팅된 정보
        self.et_tool_idt = Entry(self.settings_layer,
                                 width = 5)
        self.et_tool_idt.place(x = self.tool_ets_pos_x,
                               y = 170)
        self.inspection_option['tool']['idt'].append(self.et_tool_idt)
        self.tool_entrys.append(self.et_tool_idt)

        # IDT SUB
        self.lbl_idt = Label(self.settings_layer,
                             text = 'IDT SUB')
        self.lbl_idt.place(x = 50,
                           y = 190)

        # Spec Value (IDT SUB)
        # recipe IDT_SUB 검사 spec
        self.et_spec_idt_sub = Entry(self.settings_layer,
                                 width = 5)
        self.et_spec_idt_sub.place(x = self.spec_ets_pos_x,
                                   y = 190)
        self.inspection_option['spec']['idt_sub'].append(self.et_spec_idt_sub)
        self.spec_entrys.append(self.et_spec_idt_sub)

        # Tool Value (IDT SUB)
        # recipe IDT_SUB 검사 실제 셋팅된 정보
        self.et_tool_idt_sub = Entry(self.settings_layer,
                                 width = 5)
        self.et_tool_idt_sub.place(x = self.tool_ets_pos_x,
                                   y = 190)
        self.inspection_option['tool']['idt_sub'].append(self.et_tool_idt_sub)
        self.tool_entrys.append(self.et_tool_idt_sub)

        # PAD
        self.lbl_pad = Label(self.settings_layer,
                             text = 'PAD')
        self.lbl_pad.place(x = 50,
                           y = 210)

        # Spec Value (PAD)
        # recipe PAD 검사 spec
        self.et_spec_pad = Entry(self.settings_layer,
                                 width = 5)
        self.et_spec_pad.place(x = self.spec_ets_pos_x,
                               y = 210)
        self.inspection_option['spec']['pad'].append(self.et_spec_pad)
        self.spec_entrys.append(self.et_spec_pad)

        # Tool Value (PAD)
        # recipe PAD 검사 실제 셋팅된 정보
        self.et_tool_pad = Entry(self.settings_layer,
                                 width = 5)
        self.et_tool_pad.place(x = self.tool_ets_pos_x,
                               y = 210)
        self.inspection_option['tool']['pad'].append(self.et_tool_pad)
        self.tool_entrys.append(self.et_tool_pad)

        # Pin Mark
        self.lbl_pin_mark = Label(self.settings_layer,
                             text = 'Pin Mark')
        self.lbl_pin_mark.place(x = 50,
                                y = 230)

        # Spec Value (Pin Mark)
        # recipe Pin Mark 검사 spec
        self.et_spec_pin_mark = Entry(self.settings_layer,
                                      width = 5)
        self.et_spec_pin_mark.place(x = self.spec_ets_pos_x,
                                    y = 230)
        self.inspection_option['spec']['pin_mark'].append(self.et_spec_pin_mark)
        self.spec_entrys.append(self.et_spec_pin_mark)

        # Tool Value (Pin Mark)
        # recipe Pin Mark 검사 실제 셋팅된 정보
        self.et_tool_pin_mark = Entry(self.settings_layer,
                                      width = 5)
        self.et_tool_pin_mark.place(x = self.tool_ets_pos_x,
                                    y = 230)
        self.inspection_option['tool']['pin_mark'].append(self.et_tool_pin_mark)
        self.tool_entrys.append(self.et_tool_pin_mark)

        # Spec Values Layer
        self.lbl_spec = Label(self.settings_layer,
                              text = 'SPEC')
        self.lbl_spec.place(x = 200,
                            y = 7)


        # Tool Setting Values Layer
        self.lbl_tool = Label(self.settings_layer,
                              text = 'TOOL')
        self.lbl_tool.place(x = 320,
                            y = 7)

        



        # Check Status Layer
        # SPEC / TOOL entry 값을 서로 비교하여 같은지 아닌지 판정을 보여주는 영역
        self.lbl_check = Label(self.settings_layer,
                              text = 'CHECK')
        self.lbl_check.place(x = 440,
                             y = 7)

        # Inspection Pass Compare
        # inspection pass 개수 비교
        self.et_inspection_passes_compare = Entry(self.settings_layer,
                                                  width = 5)
        self.et_inspection_passes_compare.place(x = self.check_ets_pos_x,
                                                y = 40)
        
        self.check_entrys.append(self.et_inspection_passes_compare)

        # 1PASS Magnification Compare
        # recipe 첫번째 pass 검사 배율 비교
        self.et_1pass_check_magnification = Entry(self.settings_layer,
                                                 width = 5)
        self.et_1pass_check_magnification.place(x = self.check_ets_pos_x,
                                               y = 80)
        self.check_entrys.append(self.et_1pass_check_magnification)

        # 2PASS Magnification Compare
        # recipe 두번째 pass 검사 배율 비교
        self.et_2pass_check_magnification = Entry(self.settings_layer,
                                                 width = 5)
        self.et_2pass_check_magnification.place(x = self.check_ets_pos_x,
                                               y = 100)
        self.check_entrys.append(self.et_2pass_check_magnification)
        
        # 1PASS Illumination Compare
        # recipe 첫번째 pass 검사 밝기 비교
        self.et_1pass_check_illumination = Entry(self.settings_layer,
                                                 width = 5)
        self.et_1pass_check_illumination.place(x = self.check_ets_pos_x,
                                               y = 130)
        self.check_entrys.append(self.et_1pass_check_illumination)
        
        # 2PASS Illumination Compare
        # recipe 두번째 pass 검사 밝기 비교
        self.et_2pass_check_illumination = Entry(self.settings_layer,
                                                 width = 5)
        self.et_2pass_check_illumination.place(x = self.check_ets_pos_x,
                                               y = 150)
        self.check_entrys.append(self.et_2pass_check_illumination)

        # IDT Compare
        # recipe IDT 검사 정보 비교
        self.et_check_idt = Entry(self.settings_layer,
                                  width = 5)
        self.et_check_idt.place(x = self.check_ets_pos_x,
                                y = 170)
        self.check_entrys.append(self.et_check_idt)

        # IDT SUB Compare
        # recipe IDT_SUB 검사 정보 비교
        self.et_check_idt_sub = Entry(self.settings_layer,
                                      width = 5)
        self.et_check_idt_sub.place(x = self.check_ets_pos_x,
                                    y = 190)
        self.check_entrys.append(self.et_check_idt_sub)

        # PAD Compare
        # recipe PAD 검사 정보 비교
        self.et_check_pad = Entry(self.settings_layer,
                                  width = 5)
        self.et_check_pad.place(x = self.check_ets_pos_x,
                                y = 210)
        self.check_entrys.append(self.et_check_pad)

        # Pin Mark Compare
        # recipe Pin Mark 검사 정보 비교
        self.et_check_pin_mark = Entry(self.settings_layer,
                                      width = 5)
        self.et_check_pin_mark.place(x = self.check_ets_pos_x,
                                     y = 230)
        self.check_entrys.append(self.et_check_pin_mark)



        # main program loop
        self.window.mainloop()

    # Load 버튼을 눌렀을때 Device를 정보를 토대로 레시피 parameter 를 불러오는 여러 method집합의 wrapping method
    def load(self):
        # cluster recipe entry clear
        self.clear(self.et_cluster)
        
        # frontside recipe entry clear
        self.clear(self.et_frontside)
        
        # inspection pass entry clear
        self.clear(self.et_noip_tool)


        self.clear(self.et_tool_idt)
        self.clear(self.et_tool_idt_sub)
        self.clear(self.et_tool_pad)
        self.clear(self.et_tool_pin_mark)
        
        # cluster / frontside recipe 출력
        self.show_recipe(),
        
        # 해당 recipe의 spec 정보 출력 (미구현)
        self.show_spec()

        # 실제 recipe inspection pass의 개수 출력
        self.et_noip_tool.insert(END,self.recipe_loader.get_noip())

        # 실제 recipe inspection pass별 검사 조명 출력
        self.show_inspection_magnification()

        # 실제 recipe inspection pass별 검사 밝기 출력
        self.show_inspection_illumination()

        # 실제 recipe IDT 검사 정보 출력
        try:
            self.et_tool_idt.insert(END,self.recipe_loader.get_idt()+'um')
        except:
            self.et_tool_idt.insert(END,'')

        # 실제 recipe IDT_SUB 검사 정보 출력
        try:
            self.et_tool_idt_sub.insert(END,self.recipe_loader.get_idt_sub()+'um')
        except:
            self.et_tool_idt_sub.insert(END,'')

        # 실제 recipe PAD 검사 정보 출력
        try:
            self.et_tool_pad.insert(END, self.recipe_loader.get_pad()+'um')
        except:
            self.et_tool_pad.insert(END,'')

        # 실제 recipe Pin Mark 검사 정보 출력
        try:
            self.et_tool_pin_mark.insert(END, self.recipe_loader.get_pin_mark()+'%')
        except:
            self.et_tool_pin_mark.insert(END,'')

        # spec / tool value 비교하여 pass or ng 판정 및 출력
        self.entry_check()
        
            
    # spec / tool value 비교하여 pass or ng 판정 및 출력 method
    def entry_check(self):

        # check_entrys : 모든 check entry가 담긴 list
        # 따라서 check_entrys의 크기는 check entry의 개수이다
        # 그리고 check entry의 개수는 spec, tool entry의 개수와도 동일
        # check_entry의 개수만큼 list를 순회하며 spec ,tool entry값을 비교하여 pass or ng 출력
        for idx in range(len(self.check_entrys)):
            
            # idx번째의 entry 입력 전 초기화
            self.clear(self.check_entrys[idx])
            
            # idx번째 spec entry와 tool entry가 비어있다면 공란을 출력
            if self.spec_entrys[idx].get() == '' and self.tool_entrys[idx].get() == '':
                self.check_entrys[idx].insert(END,'')

            # idx 번째 spec entry가 tool entry와 같다면 PASS 출력
            elif self.spec_entrys[idx].get() == self.tool_entrys[idx].get():
                self.check_entrys[idx].insert(END, 'PASS')
                self.check_entrys[idx].configure(fg = 'blue')
            
            # 나머지는 전부 NG처리
            else:
                self.check_entrys[idx].insert(END,'NG')
                self.check_entrys[idx].configure(fg = 'red')
    
    # inspection pass의 검사 밝기 출력 method 
    def show_inspection_illumination(self):

        # idx번째 spec, tool의 밝기 정보가 담긴 entry를 입력 전 초기화
        for idx in range(len(self.inspection_option['tool']['illumination'])):
            self.clear(self.inspection_option['tool']['illumination'][idx])
        
        # recipe loader로 부터 inspection pass 개수를 받아와 그만큼 반복문을 수행
        # idx번째 tool밝의 정보 entry에 recipe loader의 idx를 인자로 넘겨 밝기 정보 획득, entry에 입력
        for idx in range(self.recipe_loader.get_noip()):
            self.inspection_option['tool']['illumination'][idx].insert(END,'{:.1f}'.format(float(self.recipe_loader.get_illumination(idx))))
    
    # inspection pass의 검사 배율 출력 method 
    def show_inspection_magnification(self):

         # idx번째 spec, tool의 배율 정보가 담긴 entry를 입력 전 초기화
        for idx in range(len(self.inspection_option['tool']['magnification'])):
            self.clear(self.inspection_option['tool']['magnification'][idx])

        # recipe loader로 부터 inspection pass 개수를 받아와 그만큼 반복문을 수행
        # idx번째 tool밝의 정보 entry에 recipe loader의 idx를 인자로 넘겨 밝기 정보 획득, entry에 입력
        for idx in range(self.recipe_loader.get_noip()):
            self.inspection_option['tool']['magnification'][idx].insert(END,f'{self.recipe_loader.get_magnification(idx)}')
    
    # recipe의 idt 검사 설정값 출력 method
    def show_inspetion_idt(self):

        # idt 검사 기준 입력 전 tool idt entry 초기화
        self.clear(self.inspection_option['tool']['idt'])

        # recipe laoder로 부터 recipe 설정된 idt 검사 기준 값을 획득, entry에 입력
        self.inspection_option['tool']['idt'].insert(END,self.recipe.get_idt())

    # reicpe의 idt_sub 검사 설정값 출력 method
    def show_inspection_idt_sub(self):

        # idt sub 검사 기준 입력 전 tool idt_sub entry 초기화
        self.clear(self.inspection_option['tool']['idt_sub'])

        # recipe loader로 부터 recipe 설정된 idt_sub 검사 기준 값을 획득, entry에 입력
        self.inspection_option['tool']['idt_sub'].insert(END,self.recipe.get_idt_sub())

    # recipe의 pad 검사 설정값 출력 method
    def show_inspection_pad(self):

        # pad 검사 기준 입력 전 tool pad entry 초기화
        self.clear(self.inspection_option['tool']['pad'])

        # recipe loader로 부터 recipe 설정된 pad 검사 기준 값을 획득, entry에 입력
        self.inspection_option['tool']['pad'].insert(END,self.recipe.get_pad())

    # recipe의 pin mark 검사 기준 설정값 출력 method
    def show_inspection_pin_mark(self):

        # pin mark 검사 기준 입력 전 tool pin mark entry 초기화
        self.clear(self.inspection_option['tool']['pin_mark'])

        # recipe loader로부터 recipe 설정된 pin mark 검사 기준 값을 획득, entry에 입력
        self.inspection_option['tool']['pin_mark'].insert(END,self.recipe.get_pin_mark())

    # spec recipe parameter 입력 method (미구현)
    def show_spec(self):
        pass

    # Device 입력시 cluster(PPID) reicpe와 frontside recipe 출력 method
    def show_recipe(self):

        # Device entry로 부터 입력된 정보를 인자로 RecipeLoader의 객체 생성
        # Recipe Loader는 해당 인자를 바탕으로 root path에 접근하여, xml file, tool parameter를 획득
        # 만약 Error 발생시 messagebox 출력
        try:
            self.recipe_loader = RecipeLoader(device = self.et_device.get(),layer = self.flag)
        except:
            messagebox.showerror("Not exist XML File",f"Recipe xml이 존재 하지 않습니다.")
        self.et_cluster.delete(0,"end")
        try:
            self.et_cluster.insert(0,self.recipe_loader.get_cluster())
        except:
            messagebox.showerror("Not exist Cluster Recipe",f"Cluster Recipe가 존재 하지 않습니다.")
        self.et_frontside.delete(0,"end")
        try:
            self.et_frontside.insert(0,self.recipe_loader.get_frontside())
        except:
            messagebox.showerror("Not exist Frontside Recipe",f"Frontside Recipe가 존재 하지 않습니다.")

    # AOI Layer 선택 Radio Button에 따라 Layer Flag Setting Method
    def set_flag(self):
        self.flag = self.AOI_layer.get()

    # Entry 초기화 Method
    def clear(self,widget):
        widget.delete(0,"end")
if __name__ == '__main__':
    # Main Instance 생성
    Main()