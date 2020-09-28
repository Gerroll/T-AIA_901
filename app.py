from naturalLanguageProcessing import Nlp
from pathFindingProcessing import PathFinder
from voiceProcessing import VoiceProcessing

def main():
	print('Hello world !')
	NLP = Nlp()
	NLP.train()
	print(NLP.predict("Je souhaiterai aller à Besancon"))

if __name__ == "__main__":
	main()
