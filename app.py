from naturalLanguageProcessing import Nlp
from pathFindingProcessing import PathFinder
from voiceProcessing import VoiceProcessing
import speech_recognition as sr

import sys


def main():
    voice_process = VoiceProcessing()
    # A remplacer avec la récupéation du model
    NLP = Nlp()
    NLP.train()

    try:
        # Usecase: handling from a microphone
        # resultFromVoice = voice_process.from_audio()

        # Usecase: handling from an audiofile
        resultFromVoice = voice_process.from_file(pathfile="oss117.mp4")
    except sr.RequestError as e:
        print("Connection problem, please try again later")
        return 1;
    except sr.UnknownValueError as e:
        print("Unintelligible text, please provide a new record ")
        return 1;
    try:
        start, end = NLP.predict(resultFromVoice)
    except Exception as identifier:
        print("Bad Phrase")
    if (start):
        print("Trajet", start, " - ", end)


def examples(NLP):
    # example a virer lors de l association des components
    try:
        print(NLP.predict("Je souhaiterai aller à Besancon"))
    except Exception as identifier:
        print("Bad Phrase")
    try:
        print(NLP.predict("je veux un itinéraire pour faire Montpellier - Nice"))
    except Exception as identifier:
        print("Bad Phrase")
    try:
        print(NLP.predict("je veux un itinéraire pour faire Paris - Brest"))
    except Exception as identifier:
        print("Bad Phrase")
    try:
        print(NLP.predict("je veux manger un Paris - Brest"))
    except Exception as identifier:
        print("Bad Phrase")
    try:
        print(NLP.predict("je veux manger une saucisse de Strasbourg à Brest"))
    except Exception as identifier:
        print("Bad Phrase")
    try:
        print(NLP.predict("quel est le meilleur trajet pour aller de Nice à Montpellier"))
    except Exception as identifier:
        print("Bad Phrase")
    try:
        print(NLP.predict("Paris est la meilleure ville"))
    except Exception as identifier:
        print("Bad Phrase")


if __name__ == "__main__":
    main()
