from audioAi import *
import streamlit as st
from audio_recorder_streamlit import audio_recorder
from bot_process import *
import librosa
import soundfile as sf


def skit_GUI():
    st.title("Sasta Skit")
    col1, _, col3 = st.columns(3)
    with col3:
        # Text field to put api key
        api_key = st.text_input("Enter your API key")
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
    with col1:
        audio_bytes = audio_recorder(
            text="",
            recording_color="#e8b62c",
            neutral_color="#6aa36f",
            icon_name="microphone",
            icon_size="4x",
        )
    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")
        with open("audio_data/audio.wav", "wb") as f:
            f.write(audio_bytes)
        audio_file_path = "audio_data/audio.wav"
        new_sr = 16000
        y, sr = librosa.load(audio_file_path, sr=new_sr)
        resampled_file_path = "audio_data/audio.wav"
        sf.write(resampled_file_path, y, new_sr)
        text = audioAi(audio_file_path)
        st.write(text)
        response = get_response_gpt(text)["content"]
        st.write(response)
        text_to_speech(response)
        st.audio("audio_data/output.mp3", format="audio/mp3")


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
