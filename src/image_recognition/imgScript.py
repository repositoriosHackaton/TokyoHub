import os
import cv2
import numpy as np
import random


# Function to rotate the image
def rotate_image(image, angle):
    height, width = image.shape[:2]
    rotation_matrix = cv2.getRotationMatrix2D((width/2, height/2), angle, 1)
    rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height), borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))
    return rotated_image

# Function to distort the image
def distort_image(image):
    height, width = image.shape[:2]
    distortion = np.random.normal(0, 0.5, (height, width, 3))
    distorted_image = np.clip(image + distortion * 255, 0, 255).astype(np.uint8)
    return distorted_image

# Base directory containing folders with images
base_path = r'database'
codigos_barras = ['SAM-LAV', 'SAM-MIC', 'SAM-REF', 'SAM-SEC', 'SAM-TV']

# Create variations for each image in each folder
for codigo in codigos_barras:
    folder_path = os.path.join(base_path, codigo)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)  # Create the folder if it doesn't exist
    
    image_files = os.listdir(folder_path)
    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        print(f'Processing image: {image_path}')  # Print the path of the processed image
        
        # Try to load the image
        image = cv2.imread(image_path)
        
        if image is None:
            print(f'Could not read the image: {image_path}')
            continue
        
        # Generate 100 original copies
        for i in range(1, 101):
            new_image_path = os.path.join(folder_path, f'{os.path.splitext(image_file)[0]}_original_{i}.png')
            success = cv2.imwrite(new_image_path, image)
            if success:
                print(f'Original image generated: {new_image_path}')  # Print the path of the generated image
            else:
                print(f'Error saving the image: {new_image_path}')
        
        # Generate 250 rotated variations
        for i in range(1, 251):
            angle = random.uniform(-10, 10)  # Random rotation angle between -10 and 10 degrees
            rotated_image = rotate_image(image, angle)
            new_image_path = os.path.join(folder_path, f'{os.path.splitext(image_file)[0]}_rotated_{i}.png')
            success = cv2.imwrite(new_image_path, rotated_image)
            if success:
                print(f'Rotated image generated: {new_image_path}')  # Print the path of the generated image
            else:
                print(f'Error saving the image: {new_image_path}')
        
        # Generate 250 distorted variations
        for i in range(1, 251):
            distorted_image = distort_image(image)
            new_image_path = os.path.join(folder_path, f'{os.path.splitext(image_file)[0]}_distorted_{i}.png')
            success = cv2.imwrite(new_image_path, distorted_image)
            if success:
                print(f'Distorted image generated: {new_image_path}')  # Print the path of the generated image
            else:
                print(f'Error saving the image: {new_image_path}')
        
        # Generate 300 combined variations (rotation + distortion)
        for i in range(1, 301):
            angle = random.uniform(-10, 10)  # Random rotation angle between -10 and 10 degrees
            rotated_image = rotate_image(image, angle)
            combined_image = distort_image(rotated_image)
            new_image_path = os.path.join(folder_path, f'{os.path.splitext(image_file)[0]}_combined_{i}.png')
            success = cv2.imwrite(new_image_path, combined_image)
            if success:
                print(f'Combined image generated: {new_image_path}')  # Print the path of the generated image
            else:
                print(f'Error saving the image: {new_image_path}')

print('Process completed.')

