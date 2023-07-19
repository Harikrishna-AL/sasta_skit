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

    # progress_bar = st.progress(0)
    # status_text = st.empty()
    # chart = st.line_chart(np.random.randn(10, 2))

    # for i in range(100):
    #     # Update progress bar.
    #     progress_bar.progress(i + 1)

    #     new_rows = np.random.randn(10, 2)

    #     # Update status text.
    #     status_text.text(
    #         'The latest random number is: %s' % new_rows[-1, 1])

    #     # Append data to the chart.
    #     chart.add_rows(new_rows)

    #     # Pretend we're doing some computation that takes time.
    #     time.sleep(0.1)

    # status_text.text('Done!')
    # st.balloons()
    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")


def connect_to_server():
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
