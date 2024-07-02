import tensorflow as tf
import tensorflowjs as tfjs

# Load the model from the .h5 file
model = tf.keras.models.load_model(r'C:\Users\xcrss\OneDrive - Universidad Tecnológica de Panamá\C 2\C\Code\Samsung\Proyecto_Tokyo\Tokyo_repo\model\modelo.h5')

# Convert the model to TensorFlow.js format and save it in the specified folder
tfjs.converters.save_keras_model(model, 'output')
