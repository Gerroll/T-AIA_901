from naturalLanguageProcessing import Nlp
from pathFindingProcessing import PathFinder
from voiceProcessing import VoiceProcessing
import speech_recognition as sr

import sys


def main():
	voice_process = VoiceProcessing()
	# A remplacer avec la récupéation du model
	NLP = Nlp()
	# NLP.reset()
	# NLP.train()
	examples(NLP)

	try:
		# Usecase: handling from a microphone
		# resultFromVoice = voice_process.from_audio()

		# Usecase: handling from an audiofile
		resultFromVoice = voice_process.from_file(pathfile="oss117.mp4")
		start, end = NLP.predict(resultFromVoice)
		print("Trajet", start, " - ", end)
	except sr.RequestError:
		print("Connection problem, please try again later")
		return 1
	except sr.UnknownValueError:
		print("Unintelligible text, please provide a new record ")
		return 1
	except Exception as identifier:
		print(identifier)


def examples(NLP):
	# NLP.reset()
	# NLP.train()

	# example a virer lors de l association des components
	list_text = [
		"Je souhaiterai aller à Besancon",
		"Je veux aller dans les Vosges depuis Paris",
		"Je souhaite aller de Saint-Jean-de-Védas à la gare Saint-Roch",
		"Je voudrai arriver à la gare de Lyon",
		"Je veux arriver à Paris en partant de Lille",
		"je voudrai un aller-retour Paris - Montpellier",
		"je voudrai manger une glace à Montpellier",
		"Une pizza 4 fromages Chtulhu Ftaghn"
	]
	for text in list_text:
		try:
			print(NLP.predict(text))
		except Exception as identifier:
			print(identifier)


if __name__ == "__main__":
	main()
