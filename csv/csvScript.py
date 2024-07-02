import tensorflow as tf
import numpy as np
import pandas as pd
import os
import pathlib
from tensorflow.keras.preprocessing import image
from datetime import datetime, timedelta
import random

# Define the model path
model_path = pathlib.Path(r'C:\Users\xcrss\OneDrive - Universidad Tecnológica de Panamá\C 2\C\Code\Samsung\Proyecto_Tokyo\Tokyo_repo\model\trained_model.h5')

# Load your model
model = tf.keras.models.load_model(model_path)
model.summary()  # Print model summary to inspect input shape

# Class names for each class index
class_names = ['SAM-LAV', 'SAM-MIC', 'SAM-REF', 'SAM-SEC', 'SAM-TV']

# Function to load and preprocess image
def load_and_preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(150, 150))  # Ensure target_size matches the model's input size
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0  # Normalize the image array
    return img_array

# Function to generate a random date between June 10, 2024, and June 20, 2024
def random_date(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

# Test individual predictions and save to CSV
def test_and_save_predictions(image_dir, model, output_csv):
    results = []
    start_date = datetime(2024, 6, 10)
    end_date = datetime(2024, 6, 20)
    
    for file_name in os.listdir(image_dir):
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            img_path = os.path.join(image_dir, file_name)
            img_array = load_and_preprocess_image(img_path)
            prediction = model.predict(img_array)
            predicted_class = np.argmax(prediction, axis=1)[0]
            prediction_probabilities = prediction[0]
            predicted_class_name = class_names[predicted_class]
            
            # Grouping logic for purchase and sales dates
            action_date = random_date(start_date, end_date)
            if random.random() > 0.5:
                action = 'compra'
                action_date -= timedelta(days=random.randint(0, 3))  # Purchases happen a few days before sales
            else:
                action = 'venta'
                action_date += timedelta(days=random.randint(0, 3))  # Sales happen a few days after purchases

            results.append({
                'image_name': file_name,  # Just the file name, not the full path
                'predicted_class': predicted_class_name,
                'prediction_probabilities': prediction_probabilities,
                'date': action_date.strftime('%Y-%m-%d'),
                'action': action  # Add the action column
            })
    
    # Sorting results to group purchases and sales logically
    df = pd.DataFrame(results)
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values(by=['predicted_class', 'date', 'action'], inplace=True)
    df.to_csv(output_csv, index=False)
    print(f'Results saved to {output_csv}')

# Directory containing images to classify
image_dir = pathlib.Path(r'C:\Users\xcrss\OneDrive - Universidad Tecnológica de Panamá\C 2\C\Code\Samsung\Proyecto_Tokyo\Tokyo_repo\dataset\prueba')  # Update with your directory path

# Output CSV file path
output_csv = 'predictions.csv'

# Test individual predictions and save to CSV
test_and_save_predictions(image_dir, model, output_csv)
