import whisper
import openai
from dotenv import load_dotenv
import os
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from datasets import load_dataset

load_dotenv()


def audioAi(file):
    # model = whisper.load_model("base")
    # result = model.transcribe(file)
    # audio_file = open(file, "rb")
    # result = openai.Audio.transcribe("whisper-1", audio_file)
    # return result["text"]
    processor = WhisperProcessor.from_pretrained("openai/whisper-tiny")
    model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-tiny")
    model.config.forced_decoder_ids = None

    # load dummy dataset and read audio files
    ds = load_dataset("audio_data", "clean", split="train")
    sample = ds[0]["audio"]
    input_features = processor(
        sample["array"], sampling_rate=sample["sampling_rate"], return_tensors="pt"
    ).input_features

    # generate token ids
    predicted_ids = model.generate(input_features)
    # decode token ids to text
    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=False)

    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
    # print(transcription)
    return transcription[0]


def gpt_response(text):
    out = []
    import replicate

    output = replicate.run(
        "replicate/gpt-j-6b:b3546aeec6c9891f0dd9929c2d3bedbf013c12e02e7dd0346af09c37e008c827",
        input={"prompt": text},
    )

    for item in output:
        out.append(item)
    result = ""
    for word in out:
        result += word
    return result


def text_to_speech(text):
    import requests

    CHUNK_SIZE = 1024
    url = "https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": os.getenv("XI_API_KEY"),
    }

    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.5},
    }

    response = requests.post(url, json=data, headers=headers)
    with open("audio_data/output.mp3", "wb") as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)


# if __name__ == "__main__":
#     # print(audioAi("./audio.ogg"))
#     # print(text_to_speech("Hello World"))
#     # print(gpt_response("Imagine I am a customer and you are a call center employee. I am calling you because I have a problem with my internet connection. I am very angry because I have been waiting for 2 hours. I want to cancel my subscription. Respond to me."))
#     scenario = "Imagine I am a customer and you are a call center employee from a company called Skit.AI. I am calling you because I have a problem with my internet connection. I am very angry because I have been waiting for 2 hours. I want to cancel my subscription. Respond to me accordingly now."
#     message = "Hello"
#     # query = "scenario: " + scenario + "\n\n" + "message: " + message
#     query = scenario + "\n\n" + message
#     # response = gpt_response(query)
#     # print(response)
#     # text_to_speech(response)


# load model and processor
