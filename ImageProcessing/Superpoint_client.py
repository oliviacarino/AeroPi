import socket
import cv2
import numpy as np
import pickle
import struct

# Placeholder: Replace this with your own SuperPoint processing function
def run_superpoint(image):
    # For demonstration, just using OpenCV ORB
    orb = cv2.ORB_create()
    kp = orb.detect(image, None)
    kp, des = orb.compute(image, kp)
    return kp, des

def serialize_keypoints(kp, des):
    # Keypoints can't be directly pickled, so convert to list of tuples
    kp_data = [(k.pt, k.size, k.angle, k.response, k.octave, k.class_id) for k in kp]
    return pickle.dumps((kp_data, des))

def main():
    server_ip = 'SERVER_IP_HERE'
    server_port = 12345

    cap = cv2.VideoCapture(0)  # Use Pi camera or USB cam

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        kp, des = run_superpoint(gray)

        data = serialize_keypoints(kp, des)

        # Pack message length first, then the actual data
        message = struct.pack("Q", len(data)) + data
        client_socket.sendall(message)

    cap.release()
    client_socket.close()

if __name__ == '__main__':
    main()
