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
from sasta_skit.db import (
    send_message,
    get_message_history,
    reset_database,
    dump_data_to_json,
)


def skit_GUI(
        audio_file_path,
        output_file_path,
        output_text_file_path,
        json_file_path,
        ):
    """This function is used to create the GUI for sasta Skit

    :params: None
    :return: None
    :raises: None
    """
    col11, _, col13 = st.columns(3)
    with col11:
        st.title("Sasta Skit")
    with col13:
        # place a button that can reset the output.txt file
        if st.button("Reset"):
            reset_database()
            with open(output_text_file_path, "w") as f:
                f.write("")

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
            with open(audio_file_path, "wb") as f:
                f.write(audio_bytes)

            new_sr = 16000
            y, sr = librosa.load(audio_file_path, sr=new_sr)
            sf.write(audio_file_path, y, new_sr)

            text = audioAi(file=audio_file_path)
            send_message(user_id=0, message=text)
            st.write(text)

            # combine last line from a array named output and text and don't if it's empty
            if (
                os.path.exists(output_text_file_path)
                and os.path.getsize(output_text_file_path) > 0
            ):
                with open(output_text_file_path, "r") as f:
                    last_line = f.readlines()[-1]
                if last_line:
                    text = last_line + "\n" + text
            response = get_response_gpt(input_prompt=text)
            response = response["content"]
            send_message(user_id=1, message=response)
            st.write(response)
            with open(output_text_file_path, "w") as f:
                f.write(response)

            text_to_speech(text=response, output_file_path=output_file_path)
            st.audio(
                output_file_path,
                format="audio/mp3",
            )
            user_history = get_message_history(user_id=0)
            skit_history = get_message_history(user_id=1)
            db_data = {
                "user_history": user_history,
                "skit_history": skit_history,
            }
            dump_data_to_json(data = db_data,
                              json_file_path = json_file_path,
                              )
        except Exception as e:
            st.error(e)


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
