import speech_recognition as sr
from pydub import AudioSegment
import ffmpeg
import glob

import os

# AudioSegment.ffmpeg = '/usr/local/bin/ffmpeg'

class VoiceProcessing:
    def __init__(self):
        self.recognizer = self.init_recognizer()

    def from_audio(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            print("Parlez")
            audio = self.recognizer.listen(source)
            said = ""

            try:
                said = self.recognizer.recognize_google(audio, language='fr-FR')
                print(said)
            except sr.RequestError as e:
               raise e
            except sr.UnknownValueError as e :
               raise e

        return said
        
    ### pathfile : chemin relatif depuis app.py
    #format : mp3
    def from_file(self, pathfile):
        said = ""
        if os.path.isfile(pathfile + ".mp3"):
          with open(pathfile + '.mp3') as f:
            AudioSegment.from_file(pathfile + '.mp3').export(pathfile + ".flac", "flac")

            with sr.AudioFile(pathfile + ".flac") as source:
              self.recognizer.adjust_for_ambient_noise(source)
              audio = self.recognizer.record(source, duration=10)

              os.remove(pathfile + ".flac")

              try:
                said = self.recognizer.recognize_google(audio, language='fr-FR')
              except sr.RequestError as e:
                raise e

              except sr.UnknownValueError as e:
                raise e
        else:
          print(f'File {pathfile}.mp4 does not exist.')

        return said

    ###Fonction de définition du recognizer pour en modifier les attributs, (cf Speech Recognition Library Reference)
    def init_recognizer(self):
        r = sr.Recognizer()
        r.operation_timeout = 10
        return r


