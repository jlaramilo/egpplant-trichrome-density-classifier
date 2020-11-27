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

class PredictionInputPanel(LabelFrame):
    def __init__(self, parent, img_inputs, classifier, root, app):
        self.img_inputs = img_inputs
        self.classifier = classifier

        LabelFrame.__init__(self, parent, text='Image Input/s', padx=10, pady=10, labelanchor='nw')
        self.pack(side=tk.LEFT, expand=False, fill=tk.BOTH)
        
        self.btn_select_images =  Button(self, width=12, text='Select Images', command=self.select_images)
        self.btn_select_images.grid(row=2, column=1, pady=5, sticky='e')
        
        # Create scrollbars for image listbox (lb)
        self.scrollbar_v_lb = Scrollbar(self, orient=tk.VERTICAL)
        self.scrollbar_h_lb= Scrollbar(self, orient=tk.HORIZONTAL)
        
        self.scrollbar_v_lb.grid(row=0,column=2, sticky='nws')
        self.scrollbar_h_lb.grid(row=1,column=0, columnspan=2, sticky='wse')
        
        # Display all images selected by user in a listbox
        self.listbox = Listbox(self, width=40, height=15, yscrollcommand=self.scrollbar_v_lb.set, xscrollcommand=self.scrollbar_h_lb.set)
        self.listbox.grid(row=0,column=0, columnspan=2)
        
        # Create a label that displays '[count] image/s selected'
        self.label_image_count = Label(self, width=20, padx=5, pady=3, text='No image selected.', anchor='w', borderwidth=2, relief='ridge')
        self.label_image_count.grid(row=2, column=0, sticky='w')
        
        self.classifier.model_name.set(' No model selected.')
        self.model_name_display = Entry(self, textvariable=self.classifier.model_name, width=25)
        
        self.btn_select_model =  Button(self, text='Select Model', width=12, command=lambda: self.classifier.select_model(self))
        self.btn_classify =  Button(self,text='CLASSIFY',  width=35, command=lambda: self.classifier.classify(root, app))
        
    # Might transfer the first half of this method (actual image selection part) to a separate method inside ImageData Class
    # ... and leave the 2nd half (display / view part) here
    def select_images(self):
        # Clear listbox and other lists everytime the user clicks the button and selects a new set of files 
        # ...to prevent duplicate images from being appended in the listbox
        self.listbox.delete(0, tk.END)
        self.img_inputs.selected_images.clear()
        self.img_inputs.selected_images_paths.clear()
        
        # fd.askopenfilenames() returns 'absolute' paths of the selected images. Save the paths in a list.
        self.img_inputs.selected_images_paths = list(fd.askopenfilenames(filetypes = (('jpeg files','*.jpg'), ('png files','*.png'))))
        
        # Get directory of selected images
        if len(self.img_inputs.selected_images_paths) > 0:
            self.img_inputs.selected_images_dir = os.path.dirname(self.img_inputs.selected_images_paths[0])
        
        # Display filenames/paths of selected images in listbox    
        for image_path in self.img_inputs.selected_images_paths:
         	self.listbox.insert(tk.END, image_path)
        
        # Extract just the file names from the absolue paths
        for image_path in self.img_inputs.selected_images_paths:
            filename = image_path[(len(self.img_inputs.selected_images_dir)+1):]
            self.img_inputs.selected_images.append(filename)
             
        input_count = len(self.img_inputs.selected_images)
        self.label_image_count.configure(text=str(input_count) + ' image/s selected.')
        self.show_classification_widgets()

    
    def show_classification_widgets(self):
        self.model_name_display.grid(row=4, column=0, sticky='w')
        self.btn_select_model.grid(row=4, column=1, sticky='e')
        


