# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import LabelFrame
from tkinter import Button
from tkinter import Scrollbar
from tkinter import Listbox
from tkinter import Label
from tkinter import filedialog as fd 
from tkinter import Entry
import os

class TrainInputPanel(LabelFrame):
    def __init__(self, parent, train_dir, classifier, root, app):
        self.train_dir = train_dir
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
        self.label_image_count = Label(self, width=20, padx=5, pady=3, text='No directory selected.', anchor='w', borderwidth=2, relief='ridge')
        self.label_image_count.grid(row=2, column=0, sticky='w')
        
    # Might transfer the first half of this method (actual image selection part) to a separate method inside ImageData Class
    # ... and leave the 2nd half (display / view part) here
    def select_directory(self):
        # Clear listbox and other lists everytime the user clicks the button and selects a new set of files 
        # ...to prevent duplicate images from being appended in the listbox
        self.listbox.delete(0, tk.END)
        self.train_dir = ""
        self.dir_count = 0

        # fd.askopenfilenames() returns 'absolute' paths of the selected images. Save the paths in a list.
        self.train_dir = fd.askdirectory()
        
        for i in os.listdir(self.train_dir):
            if os.path.isdir(self.train_dir+"/"+i):
                self.dir_count += 1
                self.listbox.insert(tk.END, i)
        #sort list
        temp_list = list(self.listbox.get(0, tk.END))
        temp_list.sort(key=str.lower)
        # delete contents of present listbox
        self.listbox.delete(0, tk.END)
        # load listbox with sorted data
        for item in temp_list:
            self.listbox.insert(tk.END, item)
        self.label_image_count.configure(text=str(self.dir_count) + ' classes found.')



