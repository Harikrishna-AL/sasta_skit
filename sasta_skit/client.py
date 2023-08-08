import socket
import cv2
import pickle
import struct
import imutils
import streamlit as st
import os


def client_GUI():
    # To read an play an audio file
    if os.path.exists("audio.wav"):
        audio_file = open("audio.wav", "rb")
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/wav")
    else:
        st.write("No audio file found")


def connect_to_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_ip = "192.168.29.27"
    port = 10050
    client_socket.connect((host_ip, port))
    data = b""
    payload_size = struct.calcsize("Q")

    while True:
        while len(data) < payload_size:
            packet = client_socket.recv(4 * 1024)
            if not packet:
                break
            data += packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]
        while len(data) < msg_size:
            data += client_socket.recv(4 * 1024)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)
        cv2.imshow("Receiving...", frame)
        key = cv2.waitKey(10)
        if key == 13:
            break
    client_socket.close()


client_GUI()
