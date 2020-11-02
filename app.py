from naturalLanguageProcessing import Nlp
from pathFindingProcessing import PathFinder
from voiceProcessing import VoiceProcessing
import sys

def main():
	NLP = Nlp()

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
		print(NLP.predict("quel est le meilleur trajet pour aller de Montpellier à Nice"))
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
