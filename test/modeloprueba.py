import os
import random
import shutil
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Define directories for training and validation datasets
base_path = r'C:\Users\xcrss\OneDrive - Universidad Tecnológica de Panamá\C 2\C\Code\Samsung\Proyecto_Tokyo\Tokyo_repo\src\image_recognition\database'
augmented_path = os.path.join(base_path)
train_dir = os.path.join(base_path, 'train')
valid_dir = os.path.join(base_path, 'validation')

# Define barcode categories
codigos_barras = ['SAM-LAV', 'SAM-MIC', 'SAM-REF', 'SAM-SEC', 'SAM-TV']

# Create directories for train and validation datasets
os.makedirs(train_dir, exist_ok=True)
os.makedirs(valid_dir, exist_ok=True)

# Create subdirectories for each class in train and validation directories
for codigo in codigos_barras:
    os.makedirs(os.path.join(train_dir, codigo), exist_ok=True)
    os.makedirs(os.path.join(valid_dir, codigo), exist_ok=True)

# Move files to train and validation directories (80% train, 20% validation)
for image_file in os.listdir(augmented_path):
    for codigo in codigos_barras:
        if codigo in image_file:
            src_path = os.path.join(augmented_path, image_file)
            if random.random() < 0.8:
                dst_path = os.path.join(train_dir, codigo, image_file)
            else:
                dst_path = os.path.join(valid_dir, codigo, image_file)
            shutil.move(src_path, dst_path)

print('Data splitting completed.')

# Define the simplified model
model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(16, (3, 3), activation='relu', input_shape=(150, 150, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(5, activation='softmax')  # 5 classes
])

# Compile the model
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',  # Use 'categorical_crossentropy' for one-hot encoded labels
              metrics=['accuracy'])

# Define the ImageDataGenerator for training with augmentation
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

# Define the ImageDataGenerator for validation (without augmentation)
valid_datagen = ImageDataGenerator(rescale=1./255)

# Create data generators
train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(150, 150),
    batch_size=32,
    class_mode='sparse'  # Use 'categorical' for one-hot encoded labels
)

validation_generator = valid_datagen.flow_from_directory(
    valid_dir,
    target_size=(150, 150),
    batch_size=32,
    class_mode='sparse'  # Use 'categorical' for one-hot encoded labels
)

# Train the model
history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // train_generator.batch_size,
    epochs=50,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // validation_generator.batch_size
)

# Save the model to a .h5 file
model.save('simplified_model.h5')
print('Model saved to simplified_model.h5')
