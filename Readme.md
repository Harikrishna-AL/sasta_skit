# Skit Lite (Voice AI powered by Generative AI)

This project aims to autmate call centers using vouce AI. Here, I,ll be usig OpenAI whisper and GPT models to make this possible. Right now the client and server can communicate with each other using sockets.

Different components of sasta skit:
<ul>
  <li>Streamlit GUI</li>
  <li>A LLM (here I have used chatGPT API)</li>
  <li>Whisper AI to convert audio to text</li>
  <li>Elevenlabs API for text to speech</li>
</ul>

### Blockers
Since this project was supposed to be more focused on AI rather than putting on a GUI, I initially wanted the models to run locally (at least the LLM that will generate the response). To do so the blockers were as follows:
- One such good model that I could use was LLaMA 7B model but then I needed more than 13 GB ram to load the entire model into the memory. That was the first major blocker. I solved it by using a techique called quantization. I was able to sucessfully quantize the LLaMA model to 4 bit precision. This allowed me to reduce the model size to 4.8 GB. This not only allowed me to infer the model locally but also without loosing it's quality.
- Even when I managed to run it locally. I could only infer it using a compiled binary file that I got from llama.cpp. First I tried to make a process run using python and then use threads to interact with the process by giving it inputs and then getting the stdout outputs but unfortunately, the entire wasn't synchronious and therefore I couldn't intereact with the model sucessfully.
- Even then, I tried finding other language models from hugging face but unfortunately non of the small models could produce decent enough responses even with prompt engineering. With having no choice, I had to use the openAI chatGPT API to get the results.
### How to run
- To create your own virtual environment use the following commnad
  ```shell
  virtualenv env
  source env/bin/activate
  ```
- To instal all the python package write the following command
  ```shell
  pip install git+https://github.com/Harikrishna-AL/sasta_skit.git@master#egg=sasta_skit
  ```
- To run the project using streamlit.
  Create a python file and write the following code:
  ```python
  import os

  import sasta_skit
  from sasta_skit.callBot import skit_GUI
  from dotenv import load_dotenv

  load_dotenv()

  skit = skit_GUI("/home/harikrishna/Desktop/test/audio_data/audio.wav","./audio_data/output.mp3","./output.txt")

  ```
- Now to run the project 

  ```shell
  streamlit run <name of the file>.py
  ```
### Usage

  ![image](https://github.com/Harikrishna-AL/sasta_skit/assets/91690484/3e76604a-dd9b-499a-99ac-d05c6084a298)
  
  This is how the interface for sasta skit looks. The user will have to enter their openAI api key in the api text fiels. The User can click on the microphone button to talk to the AI and thereafter, the AI will take control and give the response which will be displayed as follows. The output can be played on your speakers using the audio players.

