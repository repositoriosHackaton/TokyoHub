import os
import shutil
import random

# Define the source directories and the target directory
source_dirs = [
    'database/SAM-LAV',
    'database/SAM-MIC',
    'database/SAM-REF',
    'database/SAM-SEC',
    'database/SAM-TV'
]
target_dir = 'prueba'

# Create the target directory if it doesn't exist
os.makedirs(target_dir, exist_ok=True)

# Collect all image paths from the source directories
all_images = []
for dir_path in source_dirs:
    for file_name in os.listdir(dir_path):
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            all_images.append(os.path.join(dir_path, file_name))

# Randomly select between 40 to 70 images
num_images_to_select = random.randint(40, 70)
selected_images = random.sample(all_images, num_images_to_select)

# Copy selected images to the target directory
for img_path in selected_images:
    shutil.copy(img_path, target_dir)

print(f"Copied {len(selected_images)} images to {target_dir}")
