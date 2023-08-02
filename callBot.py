# server
import socket
import cv2
import pickle
import struct
import imutils
from audioAi import *
import streamlit as st
from audio_recorder_streamlit import audio_recorder
import numpy as np
import time


def skit_GUI():
    st.title("Sasta Skit")
    _, col2, _ = st.columns(3)
    with col2:
        audio_bytes = audio_recorder(
            text="",
            recording_color="#e8b62c",
            neutral_color="#6aa36f",
            icon_name="microphone",
            icon_size="4x",
        )
    if audio_bytes:
        # play and also save the file locally
        st.audio(audio_bytes, format="audio/wav")
        with open("audio.wav", "wb") as f:
            f.write(audio_bytes)
            


def connect_to_client():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_name = socket.gethostname()
    # host_ip = socket.gethostbyname(host_name)
    host_ip = "192.168.29.27"
    print("HOST_NAME:", host_name)
    print("HOST IP:", host_ip)
    port = 10050
    socket_address = (host_ip, port)
    print("Socket created")
    server_socket.bind(socket_address)
    print("Socket bind complete")
    server_socket.listen(5)
    print("Socket now listening")

    while True:
        client_socket, addr = server_socket.accept()
        print("Connection from:", addr)
        if client_socket:
            vid = cv2.VideoCapture(0)
            while vid.isOpened():
                img, frame = vid.read()
                a = pickle.dumps(frame)
                message = struct.pack("Q", len(a)) + a
                client_socket.sendall(message)
                cv2.imshow("Sending...", frame)
                key = cv2.waitKey(10)
                if key == 13:
                    client_socket.close()


skit_GUI()
