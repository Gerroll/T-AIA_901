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
	NLP = Nlp()

	# NLP.reset()
	# NLP.train()

	# example a virer lors de l association des components
	list_text = [
		"Je souhaiterai aller à Besancon",
		"Je souhaite aller de Saint-Jean-de-Védas à la gare de Saint-Roch",
		"Je veux arriver à la gare Saint-Moret en partant de la gare de Vichy",
		"Je veux arriver à Paris en partant de Lille",
		"je voudrai un aller-retour Paris - Montpellier",
		"je voudrai manger une glace à Montpellier",
	]
	for text in list_text:
		try:
			print(NLP.predict(text))
		except Exception as identifier:
			print(identifier)


if __name__ == "__main__":
    main()
