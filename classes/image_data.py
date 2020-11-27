# -*- coding: utf-8 -*-

from pathlib import Path
import cv2
import os
import shutil



class ImageData:
    def __init__(self):
        
        self.selected_images = []
        self.selected_images_paths = []
        self.selected_images_dir = ''
        self.input_count = 0
        self.preprocessed_images = []
        self.preprocessed_images_paths = []
        self.preprocessed_images_dir = ''
    
        
    # Other preprocessing methods to be added here in the future
    def preprocess_images(self, root, app):
    
        PROCESSED_IMAGES_DIR = "trichome_classifier/temp/processed_images"
        IMG_LENGTH = 224
        self.preprocessed_images_dir = os.path.join(self.selected_images_dir, PROCESSED_IMAGES_DIR)
        processed_images_count = 0
        
        # Crop from middle pixel. Chop off
        for i, img_path in enumerate(self.selected_images_paths):       
            img_array = cv2.imread(img_path)
            middle_y = img_array.shape[0] // 2
            new_upper_y = middle_y - (middle_y // 2)
            new_lower_y = new_upper_y + middle_y
            middle_x = img_array.shape[1] // 2
            new_left_x = middle_x - new_upper_y
            new_right_x = middle_x + new_upper_y
            img_array = img_array[new_upper_y:new_lower_y, new_left_x:new_right_x]
            img_array = cv2.resize(img_array, (IMG_LENGTH, IMG_LENGTH))
                
            # Create temporary folder where preprocessed images will be stored
            # Folder/s along will be deleted after their classes have all been predicted
            Path(self.preprocessed_images_dir).mkdir(parents=True, exist_ok=True)
            processed_img_abs_path = os.path.join(self.preprocessed_images_dir, self.selected_images[i])
            cv2.imwrite(processed_img_abs_path, img_array) 
            
            self.preprocessed_images.append(self.selected_images[i])
            self.preprocessed_images_paths.append(processed_img_abs_path)
            
            # Display updated the count of processed images on the status label
            processed_images_count += 1
            app.prediction_results_panel.str_status.set('STATUS: Preprocessing ' + str(processed_images_count) + '/' + str(len(self.selected_images_paths)) + ' images.')
            root.update()
        app.prediction_results_panel.str_status.set('STATUS: Image preprocessing done.')
        app.prediction_results_panel.label_status.configure(textvariable=app.classifier.str_status)
    

        
    # # Delete temporary files / preprocessed images
    # def cleanup(self):
    #     shutil.rmtree(self.preprocessed_images_dir)
        

                    
                
