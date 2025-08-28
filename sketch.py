import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk

images={"original":None,"sketch":None}

def open_file():
    filepath=filedialog.askopenfilename()
    if not filepath:
        return
    img=cv2.imread(filepath)
    display_img(img,original=True)
    sketch_img=convert_to_sketch(img)
    display_img(sketch_img,original=False)

def convert_to_sketch(img):
    gray_img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    inverted_img=cv2.bitwise_not(gray_img)
    blurred_img=cv2.GaussianBlur(inverted_img,(21,21),sigmaX=0,sigmaY=0)
    inverted_blur_img=cv2.bitwise_not(blurred_img)
    sketch_img=cv2.divide(gray_img,inverted_blur_img,scale=256.0)
    return sketch_img

def display_img(img,original):
    img_rgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB) if original else img
    img_pil=Image.fromarray(img_rgb)
    img_tk=ImageTk.PhotoImage(image=img_pil)

    if original:
        images["original"]=img_pil
    else:
        images["sketch"]=img_pil
    
    label=orignal_img_label if original else sketch_img_label
    label.config(image=img_tk)
    