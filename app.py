from naturalLanguageProcessing import Nlp
from pathFindingProcessing import PathFinder
from voiceProcessing import VoiceProcessing

def main():
	print('Hello world !')
	NLP = Nlp()
	NLP.train()
	try:
		print(NLP.predict("Je souhaiterai aller à Besancon"))
	except Exception as identifier:
		pass
	try:
		print(NLP.predict("je veux un itinéraire pour faire Montpellier - Nice"))
	except Exception as identifier:
		pass
	try:
		print(NLP.predict("je veux un itinéraire pour faire Paris Brest"))
	except Exception as identifier:
		pass
	try:
		print(NLP.predict("je veux manger un Paris - Brest"))
	except Exception as identifier:
		pass
	try:
		print(NLP.predict("je veux manger une saucisse de Strasbourg à Brest"))
	except Exception as identifier:
		pass


if __name__ == "__main__":
	main()
