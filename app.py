# Project libs
from naturalLanguageProcessing import Nlp
from pathFindingProcessing import PathFinder
from voiceProcessing import VoiceProcessing
from chatbot import Chatbot
import speech_recognition as sr

# Others
import sys
import requests
from rq import Queue
# import redis

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
  return 'Hello World, do you like trains ?', 200

""" CGU route """
@app.route('/cgu')
def cgu():
  return render_template('cgu.html')

""" Init chatbot, IA, and others stuff """
@app.route('/init', methods=['GET'])
def init_entry():
  # Create redis queue
  q = Queue(connection=conn)

  # Queue reset nlp
  q.enqueue(resetNlp, result_ttl=0, job_timeout=3600)

  return 'Chatbot initialized !'

""" Webhook for facebook chatbot """
@app.route('/webhook', methods=['GET', 'POST'])
def main_entry():
  # initialise components
  VP = VoiceProcessing()
  NLP = Nlp()
  PF = PathFinder()
  # initialise chatbot
  chatbot = Chatbot(VP, NLP, PF)

  # dispatch request
  res = chatbot.dispatch_request(request)

  # return result 'MESSAGE', STATUS_CODE
  return res[1], res[2]


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

