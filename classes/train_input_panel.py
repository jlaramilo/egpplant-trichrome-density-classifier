# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import LabelFrame
from tkinter import Button
from tkinter import Scrollbar
from tkinter import Listbox
from tkinter import Label
from tkinter import filedialog as fd 
from tkinter import Entry
from PIL import Image
import os, sys, time

import tensorflow as tf
import numpy as np
from glob import glob
from sklearn.model_selection import train_test_split

TRAIN_DIR = 'train'
TEST_DIR = 'test'

class TrainInputPanel(LabelFrame):
    def __init__(self, parent, img_dir, classifier, root, app):
        self.img_dir = img_dir
        self.classifier = classifier
        self.dir_count = 0

        LabelFrame.__init__(self, parent, text='Image Input/s', padx=10, pady=10, labelanchor='nw')
        self.pack(side=tk.LEFT, expand=False, fill=tk.BOTH)
        
        self.btn_select_images =  Button(self, width=12, text='Select Img Dir', command=self.select_directory)
        self.btn_select_images.grid(row=2, column=1, pady=5, sticky='e')
        
        # Create scrollbars for image listbox (lb)
        self.scrollbar_v_lb = Scrollbar(self, orient=tk.VERTICAL)
        self.scrollbar_h_lb= Scrollbar(self, orient=tk.HORIZONTAL)
        
        self.scrollbar_v_lb.grid(row=0,column=2, sticky='nws')
        self.scrollbar_h_lb.grid(row=1,column=0, columnspan=2, sticky='wse')
        
        # Display all images selected by user in a list box
        self.listbox = Listbox(self, width=40, height=15, yscrollcommand=self.scrollbar_v_lb.set, xscrollcommand=self.scrollbar_h_lb.set)
        self.listbox.grid(row=0,column=0, columnspan=2)
        
        # Create a label that displays '[count] image/s selected'
        self.label_image_count = Label(self, width=25, padx=5, pady=3, text='No directory selected.', anchor='w', borderwidth=2, relief='ridge')
        self.label_image_count.grid(row=2, column=0, sticky='w')

        self.btn_select_images =  Button(self, width=40, text='Preprocess training and test data', command=self.preprocess_data)
        self.btn_select_images.grid(row=3, column=0, columnspan=2 , sticky='w')
        
        #progress data processing
        self.data_progress = Label(self, text='Processing data...', width=25)
    # Might transfer the first half of this method (actual image selection part) to a separate method inside ImageData Class
    # ... and leave the 2nd half (display / view part) here
    def select_directory(self):
        # Clear listbox and other lists everytime the user clicks the button and selects a new set of files 
        # ...to prevent duplicate images from being appended in the listbox
        self.listbox.delete(0, tk.END)
        self.img_dir = ""
        self.dir_count = 0

        # fd.askopenfilenames() returns 'absolute' paths of the selected images. Save the paths in a list.
        self.img_dir = fd.askdirectory()
        
        for i in os.listdir(self.img_dir):
            if os.path.isdir(self.img_dir+"/"+i):
                self.dir_count += 1
                self.listbox.insert(tk.END, i)
        #sort list
        temp_list = list(self.listbox.get(0, tk.END))
        temp_list.sort(key=str.lower)
        self.listbox.delete(0, tk.END)
        for item in temp_list:
            self.listbox.insert(tk.END, item)
            
        self.label_image_count.configure(text=str(self.dir_count) + ' classes found.')
    
    def preprocess_data(self):
        
        self.data_progress.grid(row=4, column=0, columnspan=2 , sticky='w')

        os.system('mkdir train')
        os.system('mkdir test')
        
        for item in os.listdir(self.img_dir):
            os.system('mkdir train/'+str(item))
            for i,items in enumerate(os.listdir(self.img_dir+"/"+item)):
                im = Image.open(self.img_dir+"/"+item+"/"+items)
                w, h = im.size
                f, e = os.path.splitext(items)

                imResize = im.resize((w//2,h//2), Image.ANTIALIAS)
                imResize.save("train/" + item + "/100" + str(i) + '.jpg', 'JPEG', quality=90)
                    
                imFlipH = imResize.transpose(Image.FLIP_LEFT_RIGHT)
                imFlipH.save("train/" + item + "/100" + str(i) + "_flipH" + '.jpg', 'JPEG', quality=90)

                imFlipV = imResize.transpose(Image.FLIP_TOP_BOTTOM)
                imFlipV.save("train/" + item + "/100" + str(i) + "_flipV" + '.jpg', 'JPEG', quality=90)

                for j in range(90,360,90):
                    imRotate = imResize.rotate(j)
                    imRotate.save("train/" + item + "/100" + str(i) + "_rotate"+ str(j) + '.jpg', 'JPEG', quality=90)


            classification = glob('train/'+str(item)+'/*.jpg')
            class_train, class_test = train_test_split(classification, test_size=0.30)
            
            os.system('mkdir test/'+str(item))
            files = ' '.join(class_test)
            os.system('mv -t test/'+str(item)+' '+files)

        self.data_progress['text'] = 'Done.'
        


    def show_data_progress(self):
        self.data_progress.grid(row=4, column=0, sticky='w')