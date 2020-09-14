import speech_recognition as sr


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
                print("Connection problem, please try again later")
            except sr.UnknownValueError as e :
                print("Unintelligible text, please provide a new record ")

        return said
    ### pathfile : chemin relatif depuis app.py
    def from_file(self, pathfile):
        r = sr.Recognizer()

        source = sr.AudioFile(pathfile)
        with source:
            r.adjust_for_ambient_noise(source)
            audio = r.record(source)

            said = ""

            try:
                said = r.recognize_google(audio, language='fr-FR')
                print(said)
            except sr.RequestError as e:
                print("Connection problem, please try again later")

            except sr.UnknownValueError as e:
                print("Unintelligible text, please provide a new record ")

        return said

        print(r.recognize_google(audioToAnalyze, language='fr-FR'))

    ###Fonction de définition du recognizer pour en modifier les attributs, (cf Speech Recognition Library Reference)
    def init_recognizer(self):
        r = sr.Recognizer()
        r.operation_timeout = 10
        return r


