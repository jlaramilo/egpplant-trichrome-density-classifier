# -*- coding: utf-8 -*-

from tkinter import Frame
from tkinter import ttk
from classes.image_data import ImageData
from classes.classifier import Classifier
from classes.train_input_panel import TrainInputPanel
from classes.prediction_input_panel import PredictionInputPanel
from classes.prediction_results_panel import PredictionResultsPanel

class Application:
    def __init__(self, master):
        self.master = master
        master.geometry('850x420')
        master.title('Eggplant Trichome Density Classifier')
        # master.iconbitmap('resources/icons/eggplant_icon.ico')
        
        self.training_directory = ""
        self.prediction_input_images = ImageData()
        self.classifier = Classifier(self.prediction_input_images)
        
        self.load_widgets()
        
        
    def load_widgets(self):
        # Create a notebook that will manage the tabs
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(pady=3)
        
        self.frm_train_tab = Frame(self.notebook, width=900, height=420, bg='yellow')
        self.frm_train_tab.pack(fill="both", expand=1)
        
        self.frm_predict_tab = Frame(self.notebook, width=900, height=420, bg='blue')
        self.frm_predict_tab.pack(fill="both", expand=1)
        
        self.notebook.add(self.frm_train_tab, text="Train")
        self.notebook.add(self.frm_predict_tab, text="Predict")
        
        self.train_input_panel = TrainInputPanel(self.frm_train_tab, self.training_directory, self.classifier, self.master, self)

        self.prediction_input_panel = PredictionInputPanel(self.frm_predict_tab, self.prediction_input_images, self.classifier, self.master, self)
        self.prediction_results_panel = PredictionResultsPanel(self.frm_predict_tab, self.prediction_input_images, self.classifier, self.master, self)
        

    
    
    
        
        