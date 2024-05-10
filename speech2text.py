import os
import warnings
import speech_recognition as sr
from pydub import AudioSegment

warnings.filterwarnings('ignore')


def speech2text(filename=None):
    if filename is None:
        filename = "Arduino_Text[Me].wav"

    audio_file = filename
    audio = AudioSegment.from_wav(audio_file)
    temp_file = "temp.wav"
    audio.export(temp_file, format="wav")
    r = sr.Recognizer()
    with sr.AudioFile(temp_file) as source:
        audio_data = r.record(source)
        try:
            text = r.recognize_google(audio_data, language="ru-RU")
            return text
        except sr.UnknownValueError:
            print("Google Web Speech API could not understand the audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Web Speech API; {str(e)}")
    os.remove(temp_file)


print(speech2text('output.wav'))
