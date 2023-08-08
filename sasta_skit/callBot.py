import os

import streamlit as st
from audio_recorder_streamlit import audio_recorder
import librosa
import soundfile as sf

from sasta_skit.bot_process import get_response_gpt
from sasta_skit.audioAi import (
    audioAi,
    text_to_speech,
)


def skit_GUI():
    """This function is used to create the GUI for sasta Skit

    :params: None
    :return: None
    :raises: None
    """
    st.title("Sasta Skit")
    col1, _, col3 = st.columns(3)

    with col3:
        api_key = st.text_input("Enter your API key")
        try:
            os.environ["OPENAI_API_KEY"] = api_key
        except Exception as e:
            st.error(e)
    with col1:
        audio_bytes = audio_recorder(
            text="",
            recording_color="#e8b62c",
            neutral_color="#6aa36f",
            icon_name="microphone",
            icon_size="4x",
        )

    if audio_bytes:
        try:
            st.audio(audio_bytes, format="audio/wav")
            with open("audio_data/audio.wav", "wb") as f:
                f.write(audio_bytes)

            audio_file_path = "audio_data/audio.wav"
            new_sr = 16000
            y, sr = librosa.load(audio_file_path, sr=new_sr)
            resampled_file_path = "audio_data/audio.wav"
            sf.write(resampled_file_path, y, new_sr)

            text = audioAi(file=audio_file_path)
            st.write(text)

            # combine last line from output.txt and text and don't if it's empty
            if os.path.exists("output.txt") and os.path.getsize("output.txt") > 0:
                with open("output.txt", "r") as f:
                    last_line = f.readlines()[-1]
                if last_line:
                    text = last_line + '\n' + text
            
            response = get_response_gpt(input_prompt=text)["content"]
            st.write(response)
            with open('output.txt', 'w') as f:
                f.write(response)

            text_to_speech(text=response)
            st.audio(
                "audio_data/output.mp3",
                format="audio/mp3",
            )
        except Exception as e:
            st.error(e)

skit_GUI()


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


