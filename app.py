# Project libs
from naturalLanguageProcessing import Nlp
from pathFindingProcessing import PathFinder
from voiceProcessing import VoiceProcessing
from controllers import MainController
import speech_recognition as sr

# Others
import sys
import os
import requests

# Flask
from flask import Flask, session, request, render_template, redirect, url_for

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_8#y2o"J4Q9z\n\xec]/'

# initialise components
VP = VoiceProcessing()
NLP = Nlp()
PF = PathFinder()
print('Done initialisation component')

def resetNlp():
  NLP = Nlp()
  NLP.reset()
  NLP.train()
  NLP.test()

""" Reset Nlp route """
@app.route('/reset')
def reset():
  resetNlp()

  return "Nlp a été reset avec succès."

""" Home route """
@app.route('/')
def home():
  # generate uniq id for our user
  if 'userId' not in session:
    userId = os.urandom(16)
    session['userId'] = userId

  # clean session for result
  if 'result' in session:
    session.pop('result')


  # render home page
  return render_template('home.html')

""" Result route """
@app.route('/result')
def result():
  # store it in session
  if 'userId' in session and 'result' in session:
    # render result page
    return render_template('result.html')
  else:
    return redirect(url_for('home'))

""" Process route """
@app.route('/process', methods=['POST'])
def process():
  # clean session errors
  if 'errors' in session:
    session.pop('errors')
  userId = request.form['userId']
  audio = request.files['audio']
  # get the userId in request args and check it's egal to our session['userId]
  if session['userId'] and str(userId) == str(session['userId']):
    # initialise main controller
    processor = MainController(VP, NLP, PF)
    # dispatch request
    res = processor.process_audio(audio)

    if int(res[1]) == 666: # Error
      # save error message to session
      session['errors'] = res[0]
    else:
      # save result to session
      session['result'] = res[0]

    # return result status
    return dict({'status': res[1]})
  else:
    return dict({'status': 401})



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

