import sys
sys.path.append('/home/hammad/FYP/Kivy/Testing')

import os
import random
import numpy as np

# Fix seeds before importing TensorFlow.
os.environ['PYTHONHASHSEED'] = '0'
np.random.seed(0)
random.seed(0)
import tensorflow as tf


from tensorflow.keras.applications import VGG16
from tensorflow.keras.layers import GlobalAveragePooling2D
from tensorflow.keras.preprocessing import image as img_preprocessing

tf.random.set_seed(0)

from database import test3




# Load the VGG16 model without the top classification layers
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Freeze the pre-trained layers
for layer in base_model.layers:
    layer.trainable = False

# # Add global average pooling and dense layers for feature extraction
model = tf.keras.Sequential([
    base_model,
    GlobalAveragePooling2D(),
    tf.keras.layers.Dense(1024, activation='relu', dtype='float64')
])

# features' extraction
def extract_features(image_path):
    img = img_preprocessing.load_img(image_path, target_size=(224, 224))
    img_array = img_preprocessing.img_to_array(img)
    img_batch = np.expand_dims(img_array, axis=0)
    img_preprocessed = tf.keras.applications.vgg16.preprocess_input(img_batch)

    features = model.predict(img_preprocessed)
    features = features.flatten()  # Flatten to a 1D feature vector
    features = features.tolist()
    return features




def process_data(details_instance):
    # Access attributes using the instance
    name = details_instance.username
    age = details_instance.age
    gender = details_instance.gender
    state = details_instance.state
    picture_file_path = details_instance.picture_file_path
    radiograph_file_path = details_instance.radiograph_file_path
        
    # Extract features from the new image
    extracted_features = extract_features(radiograph_file_path)
    
    # # send to database
    test3.db_operations(name, age, gender, state, picture_file_path, radiograph_file_path,  extracted_features )



    # Add more processing logic as needed



