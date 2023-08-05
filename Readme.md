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
  
