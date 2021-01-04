# Project libs
from naturalLanguageProcessing import Nlp
from pathFindingProcessing import PathFinder
from voiceProcessing import VoiceProcessing
from controllers import MainController
import speech_recognition as sr

# Others
import sys
import requests

# Flask
from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)

def resetNlp():
  NLP = Nlp()
  NLP.reset()
  NLP.train()
  NLP.test()

""" Just home route """
@app.route('/')
def home():
  # generate uniq id for our user
  uniqid = 'AUHzdqoid561&é"'
  # render home page
  return render_template('home.html')

""" Process route """
@app.route('/process', methods=['POST'])
def process():
  # initialise components
  VP = VoiceProcessing()
  NLP = Nlp()
  PF = PathFinder()
  # initialise chatbot
  processor = MainController(VP, NLP, PF)

  # dispatch request
  res = processor.process_post_request(request)

  # return result 'MESSAGE', STATUS_CODE
  # return res[1], res[2]

  # render template result
  return render_template('result.html')



""" Main program """
def main():

	voice_process = VoiceProcessing()
	# A remplacer avec la récupéation du model
	NLP = Nlp()
 
	### a enlever si l'entrainement n'est pas nécessaire pour vous
	# NLP.reset()
	# NLP.train(n_iter=100)
	###

	NLP.test()

	try:
		# Usecase: handling from a microphone
		resultFromVoice = voice_process.from_audio()

		# Usecase: handling from an audiofile
		# resultFromVoice = voice_process.from_file(pathfile="oss117.mp4")

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

if __name__ == "__main__":
  # Reset NLP by hand if you want a MAJ on it before pushing repo into production (heroku)
  resetNlp()

