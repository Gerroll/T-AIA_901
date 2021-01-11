from naturalLanguageProcessing import Nlp
from pathFindingProcessing import PathFinder
from voiceProcessing import VoiceProcessing
import speech_recognition as sr

import sys

def main():
	voice_process = VoiceProcessing()
	# A remplacer avec la récupéation du model
	NLP = Nlp()

	### a enlever si l'entrainement n'est pas nécessaire pour vous
	# NLP.reset()
	# NLP.train(n_iter=400)
	###

	NLP.test()

	try:
		# # Usecase: handling from a microphone
		# resultFromVoice = voice_process.from_audio()

		# # Usecase: handling from an audiofile
		# # resultFromVoice = voice_process.from_file(pathfile="oss117.mp4")

		# start, end = NLP.predict(resultFromVoice)
		# print("Trajet", start, " - ", end)
		pass
	except sr.RequestError:
		print("Connection problem, please try again later")
		return 1
	except sr.UnknownValueError:
		print("Unintelligible text, please provide a new record ")
		return 1
	except Exception as identifier:
		print(identifier)

if __name__ == "__main__":
	main()
