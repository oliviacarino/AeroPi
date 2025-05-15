import socket
import pickle
import struct
import cv2
import numpy as np

def deserialize_keypoints(kp_data, des):
    keypoints = []
    for pt, size, angle, response, octave, class_id in kp_data:
        kp = cv2.KeyPoint(x=pt[0], y=pt[1], _size=size, _angle=angle,
                          _response=response, _octave=octave, _class_id=class_id)
        keypoints.append(kp)
    return keypoints, des

def main():
    host_ip = '0.0.0.0'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host_ip, port))
    server_socket.listen(5)
    print(f"Listening on {host_ip}:{port}...")

    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")

    data_buffer = b""
    payload_size = struct.calcsize("Q")

    while True:
        while len(data_buffer) < payload_size:
            data_buffer += conn.recv(4096)
        packed_msg_size = data_buffer[:payload_size]
        data_buffer = data_buffer[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        while len(data_buffer) < msg_size:
            data_buffer += conn.recv(4096)

        frame_data = data_buffer[:msg_size]
        data_buffer = data_buffer[msg_size:]

        kp_data, des = pickle.loads(frame_data)
        keypoints, des = deserialize_keypoints(kp_data, des)

        # Visualize keypoints on a blank image
        img = np.zeros((480, 640), dtype=np.uint8)
        out_img = cv2.drawKeypoints(img, keypoints, None, color=(0, 255, 0))
        cv2.imshow("Received SuperPoint Features", out_img)

        if cv2.waitKey(1) == 27:
            break

    conn.close()
    server_socket.close()

if __name__ == '__main__':
    main()
