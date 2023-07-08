import whisper

def audioAi(file):
    model = whisper.load_model("base")
    result = model.transcribe(file)
    return result["text"]

if __name__ == "__main__":
    print(audioAi("./audio.ogg"))