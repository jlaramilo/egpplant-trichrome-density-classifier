# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import LabelFrame
from tkinter import Label
from tkinter import Listbox
from tkinter import StringVar
from tkinter import Button

class PredictionResultsPanel(LabelFrame):
    def __init__(self, parent, img_data, classifier, root, app):
        self.img_data = img_data
        self.classifier = classifier 
        
        LabelFrame.__init__(self, parent, text='Results', padx=10, pady=10, labelanchor='nw')
        
        self.str_status = StringVar()
        self.str_status.set('STATUS: ')
       
        self.pack(side=tk.LEFT, expand=False, fill=tk.BOTH)
        self.label_few = Label(self, text='Few: ', width=18, padx=3, pady=5, anchor='w')
        self.label_intermediate = Label(self, text='Intermediate: ', width=18, padx=3, pady=5, anchor='w')
        self.label_dense = Label(self, text='Dense: ', width=18, padx=3, pady=5, anchor='w')
        self.label_very_dense = Label(self, text='Very Dense: ', width=18, padx=3, pady=5, anchor='w')
                
        self.label_few.grid(row=1, column=0, sticky='w')
        self.label_intermediate.grid(row=1, column=1, sticky='w')
        self.label_dense.grid(row=1, column=2, sticky='w')
        self.label_very_dense.grid(row=1, column=3, sticky='w')
        
        self.label_status = Label(self, textvariable=self.str_status, width=75, padx=3, pady=5, anchor='w', borderwidth=2, relief='ridge')
        self.label_status.grid(row=0, column=0, columnspan = 4, sticky='w')
        
        self.str_few_stats = StringVar()
        self.str_few_stats.set('Few: ')
        self.str_intermediate_stats = StringVar()
        self.str_intermediate_stats.set('Intermediate: ')
        self.str_dense_stats = StringVar()
        self.str_dense_stats.set('Dense: ')
        self.str_very_dense_stats = StringVar()
        self.str_very_dense_stats.set('Very Dense: ')
        
        self.label_few = Label(self, textvariable=self.str_few_stats, width=18, padx=3, pady=5, anchor='w')
        self.label_few.grid(row=1, column=0, sticky='w')
        self.label_intermediate = Label(self, textvariable=self.str_intermediate_stats,  width=18, padx=3, pady=5, anchor='w')
        self.label_intermediate.grid(row=1, column=1, sticky='w')
        self.label_dense = Label(self, textvariable=self.str_dense_stats, width=18, padx=3, pady=5, anchor='w')
        self.label_dense.grid(row=1, column=2, sticky='w')
        self.label_very_dense = Label(self, textvariable=self.str_very_dense_stats, width=18, padx=3, pady=5, anchor='w')
        self.label_very_dense.grid(row=1, column=3, sticky='w')
        
        self.listbox_few = Listbox(self, width=19, height=13)
        self.listbox_few.grid(row=2,column=0, sticky='w')
        self.listbox_intermediate = Listbox(self, width=19, height=13)
        self.listbox_intermediate.grid(row=2,column=1, sticky='w')
        self.listbox_dense = Listbox(self, width=19, height=13)
        self.listbox_dense.grid(row=2,column=2, sticky='w')
        self.listbox_very_dense = Listbox(self, width=19, height=13)
        self.listbox_very_dense.grid(row=2,column=3, sticky='w')
        
        self.button_save_results =  Button(self, width=15, text="Save Results", command=lambda:self.classifier.save_results(app), state=tk.DISABLED)
        self.button_save_results.grid(row=3, column=3, pady=5, sticky='w')
        



