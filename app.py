from naturalLanguageProcessing import Nlp
from pathFindingProcessing import PathFinder
from voiceProcessing import VoiceProcessing
import speech_recognition as sr


def main():
	voice_process = VoiceProcessing()
	try:
		resultFromVoice = voice_process.from_audio()
		#Usecase: handling from an audiofile
	    #resultFromVoice = voice_process.from_file(pathfile="test_reco.flac")

	except sr.RequestError as e:
		print("Connection problem, please try again later")
		return 1;
	except sr.UnknownValueError as e:
		print("Unintelligible text, please provide a new record ")
		return 1;

	#Use resultFromVoice for next step



if __name__ == "__main__":
	main()
