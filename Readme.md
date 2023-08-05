# Skit Lite

This project aims to autmate call centers using vouce AI. Here, I,ll be usig OpenAI whisper and GPT models to make this possible. Right now the client and server can communicate with each other using sockets.

Different components of sasta skit:
<ul>
  <li>Streamlit GUI</li>
  <li>A LLM (here I have used chatGPT API)</li>
  <li>Whisper AI to convert audio to text</li>
  <li>Elevenlabs API for text to speech</li>
</ul>

### How to run
- To create your own virtual environment use the following commnad
  ```
  virtualenv env
  ```
- To instal all the python dependencies write the following command
  ```
  pip install -r skit-requirements.txt
  ```
- To run the project using streamlit.
  ```
  streamlit run callBot.py
  ```
### Usage

  ![image](https://github.com/Harikrishna-AL/sasta_skit/assets/91690484/3e76604a-dd9b-499a-99ac-d05c6084a298)
  
  This is how the interface for sasta skit looks. The user will have to enter their openAI api key in the api text fiels. The User can click on the microphone button to talk to the AI and thereafter, the AI will take control and give the response which will be displayed as follows. The output can be played on your speakers using the audio players.

