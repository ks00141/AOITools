'''
211207 - ROI Image 획득 문제로 개발 잠정 보류
'''

from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import os

class ImageLoader():
    def __init__(self,root_window, path = None):
        self.root_window = root_window
        self.ROI_ROOT = '\\\\10.21.10.204\\fab 기술\\fab기술\\00_BackPart\\06_심영현\\레시피 점검\\ROI'
#        '\\\\10.21.10.204\\fab 기술\\fab기술\\00_BackPart\\06_심영현\\레시피 점검\\ROI'

    def show_roi(self,device,inspection_pass = '1pass'):

        try:
            self.img_path = os.path.join(self.ROI_ROOT,device.upper(),f'{inspection_pass}.jpg'.upper())
            print(self.img_path)
            self.image = Image.open(self.img_path)
            self.img_size = self.image.size
            self.img_width = self.img_size[0]
            self.img_height = self.img_size[1]
            self.sub_window = Toplevel(self.root_window)
            self.sub_window.geometry(f'{self.img_width}x{self.img_height}')
            self.canvas_roi_img = Canvas(self.sub_window,
                                        width = self.img_width,
                                        height = self.img_height)
            self.canvas_roi_img.pack()
            self.img_path = ImageTk.PhotoImage(image = self.image,master = self.sub_window)
            print(self.img_path._PhotoImage__size)
            self.canvas_roi_img.create_image(self.img_width/2,self.img_height/2,image = self.img_path)
        except:
            messagebox.showerror("Not exist ROT image",f"{device} ROI 이미지가 존재 하지 않습니다.")

        