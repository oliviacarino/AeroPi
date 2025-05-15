import cv2
import numpy as np
import tensorflow as tf
import json

# Load SuperPoint TFLite model
interpreter = tf.lite.Interpreter(model_path="superpoint.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Load and preprocess image (grayscale, 1xHxWx)
img = cv2.imread("image.jpg", cv2.IMREAD_GRAYSCALE)
img_resized = cv2.resize(img, (320, 240))  # Must match model input
img_input = img_resized.astype(np.float32) / 255.0
img_input = img_input[np.newaxis, :, :, np.newaxis]  # (1, H, W, 1)

# Run inference
interpreter.set_tensor(input_details[0]['index'], img_input)
interpreter.invoke()

# Extract outputs
keypoints = interpreter.get_tensor(output_details[0]['index'])[0]  # shape: [num_kp, 2]
descriptors = interpreter.get_tensor(output_details[1]['index'])[0]  # shape: [num_kp, 256]

# Save results
output = {
    "keypoints": keypoints.tolist(),
    "descriptors": descriptors.tolist(),
    "image_shape": img.shape
}

with open("features_image1.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"Extracted {len(keypoints)} keypoints.")
