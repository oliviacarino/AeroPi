import os
from PIL import Image
import numpy as np
import tensorflow as tf

put_details = interpreter.get_output_details()

model = tf.keras.models.load_model('dncnn.h5', compile=False)

def preprocess_image(image_path):
    img = Image.open(image_path).convert('RGB')  # convert to RGB
    #img = img.resize((128, 128))
    img = img.resize((1024,1024)) # decrease this if you have a low-end computer / GPU :'(
    img_np = np.array(img, dtype=np.float32) / 255.0
    img_np = img_np[np.newaxis, :, :, :]  # shape (1, 128, 128, 3)
    return img_np


def denoise_image(input_image):
    output_data = model.predict(input_image)
    output_image = np.squeeze(output_data) * 255.0
    output_image = np.clip(output_image, 0, 255).astype(np.uint8)
    return Image.fromarray(output_image)

input_dir = "images/south-building/images/"
output_dir = "denoised-images/"

for filename in os.listdir(input_dir):
    if filename.lower().endswith(('.jpg')):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)

        input_img = preprocess_image(input_path)
        clean_img = denoise_image(input_img)
        clean_img.save(output_path)

        print(f"Denoised and saved: {output_path}")
