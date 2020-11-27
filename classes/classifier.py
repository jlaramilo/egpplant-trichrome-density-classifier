# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import StringVar
from tkinter import Label
from tkinter import Button
from tkinter import filedialog as fd 
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.preprocessing import image
import os
import numpy as np

class Classifier:
    
    def __init__(self, img_inputs):
        self.img_inputs = img_inputs
        self.selected_model_path = ''
        self.model_name = StringVar()
        self.model_name.set('No model selected.')
        
        self.dense_list = []
        self.few_list = []
        self.intermediate_list = []
        self.very_dense_list = []
        
        # Current available model I trained/saved has the ff index-to-class mapping- 0: dense, 1: few, 2: intermediate, 3: very_dense
        self.class_labels = ["dense", "few", "intermediate", "very dense"]
        
        self.str_status = StringVar()
        self.str_status.set('STATUS: ')
              
    
    def select_model(self, input_panel):
        self.selected_model_path = fd.askopenfilename(filetypes = (('h5 files','*.h5'), ('hdf5 files','*.hdf5')))
        self.model_name.set(self.selected_model_path)
        if len(self.selected_model_path) > 0:
            input_panel.btn_classify.grid(row=5, column=0, columnspan=2, pady=5, sticky='w')
            
    def classify(self, root, app):
        # Preprocess input images (resize, sharpen, etc.)
        self.img_inputs.preprocess_images(root, app)

        model = load_model(self.selected_model_path)
        
        # for idx, img in enumerate(self.img_inputs.preprocessed_images_paths):
        for idx, img in enumerate(os.listdir(self.img_inputs.preprocessed_images_dir)):
            
            self.str_status.set('STATUS: Classifying ' + str(idx+1) + '/' + str(len(self.img_inputs.preprocessed_images_paths)) + ' images.')
            root.update()
            loaded_img = image.load_img(os.path.join(self.img_inputs.preprocessed_images_dir, img), target_size=(224, 224))
            # loaded_img = image.load_img((img), target_size=(224, 224))
            img_array = image.img_to_array(loaded_img)
            
            # Forgot why I named it img_batch lol
            img_batch = np.expand_dims(img_array, axis=0)
            
            # preprocess_input = built-in keras fxn that preprocesses images based on current pre-trained framework (in this case, VGG) 
            # VGG16 preprocess_input fxn: 
            # ... 1) Converts the image(s) from RGB to BGR 
            # ... 2) Subtracts the dataset mean from the image(s) 
            img_preprocessed = preprocess_input(img_batch)
            
            # Returns a list of the probabiblities of an image belonging to a class
            # e.g. prediction = [0.10, 0.15, 0.60, 0.05] = 60% chance that image belongs to intermediate class
            prediction = model.predict(img_preprocessed)
            
            # Returns the index of the class with the highest probability
            result = np.argmax(prediction, axis=-1)
            
            # Code can still be refactored
            # Add the image names to their respective predicted classes and update listbox
            if result[0] == 0:
                self.dense_list.append(img)
                app.prediction_results_panel.str_dense_stats.set('Dense: ' + str(len(self.dense_list)) + ' (' + str((round(len(self.dense_list)/len(self.img_inputs.preprocessed_images_paths), 2)) * 100) + '%)')
                app.prediction_results_panel.listbox_dense.insert(tk.END, img)
            elif result[0] == 1:
                self.few_list.append(img)
                app.prediction_results_panel.str_few_stats.set('Few: ' + str(len(self.few_list)) + ' (' + str((round(len(self.few_list)/len(self.img_inputs.preprocessed_images_paths), 2)) * 100) + '%)')
                app.prediction_results_panel.listbox_few.insert(tk.END, img)
            elif result[0] == 2:
                self.intermediate_list.append(img)
                app.prediction_results_panel.str_intermediate_stats.set('Intermediate: ' + str(len(self.intermediate_list)) + ' (' + str((round(len(self.intermediate_list)/len(self.img_inputs.preprocessed_images_paths), 2)) * 100) + '%)')
                app.prediction_results_panel.listbox_intermediate.insert(tk.END, img)
            elif result[0] == 3:
                self.very_dense_list.append(img)
                app.prediction_results_panel.str_very_dense_stats.set('Very Dense: ' + str(len(self.very_dense_list)) + ' (' + str((round(len(self.very_dense_list)/len(self.img_inputs.preprocessed_images_paths), 2)) * 100) + '%)')
                app.prediction_results_panel.listbox_very_dense.insert(tk.END, img)  
                
        app.prediction_results_panel.button_save_results.configure(state=tk.NORMAL)

    def save_results(self, app):
        file_name = fd.asksaveasfilename(title = 'Save file as...', filetypes = (('txt file','*.txt'),))
        
        if len(file_name) > 0:
            
            f = open(file_name + str('.txt'), 'a')
            
            # Write results in a txt file in <image_name, classification> format
            for img in self.few_list:
                f.write(img + ', few\n')
            for img in self.intermediate_list:
                f.write(img + ', intermediate\n')
            for img in self.dense_list:
                f.write(img + ', dense\n')
            for img in self.very_dense_list:
                f.write(img + ', very dense\n')
            f.close()
    
            popup = tk.Tk()
            label = Label(popup, text='Results saved in ' + file_name + '.txt')
            label.pack(side="top", fill="x", pady=10)
            button_ok = Button(popup, text="Okay", command=popup.destroy)
            button_ok.pack()
            popup.mainloop()
            # self.img_inputs.cleanup()


    