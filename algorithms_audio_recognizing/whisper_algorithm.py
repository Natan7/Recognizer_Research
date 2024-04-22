import whisper
from output_recognizer import output

def whisper(mp3_file, file_name, folder):
    speech_model = whisper.load_model("small")
    response = speech_model.transcribe(mp3_file)
    output(folder, file_name, response["text"])
    return response["text"]