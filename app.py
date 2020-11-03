# Project libs
from naturalLanguageProcessing import Nlp
from pathFindingProcessing import PathFinder
from voiceProcessing import VoiceProcessing
import speech_recognition as sr

# Others
import sys
import requests
import os
import time
from rq import Queue
from worker import conn
import redis

# Flask
from flask import Flask
from flask import request
from flask import abort

app = Flask(__name__)

# Verify token. Should be a random string.
VERIFY_TOKEN = "EAAwCqdXoSnYBANZCKxZAZAp7Xu4bwwJ6ZCUSIEa7gHvQt55oDielASlZB6ipIwdZCsNTkysCK3eYZCZCZAnowwRXz2twu4RTo1yWvfm77cGsGu6XMlAgXtN89Nerqg5iQhUiLq54DxP4j57xOY3BqNlzchEzeP740wAP8IhROfhLyXwZDZD"
ACCESS_TOKEN = "EAAwCqdXoSnYBAGvZAVkROulrJLGagS2DgeAo2SaHMlbZAvZAOflFgm1TuzR2QeWhmJt6OpbQZBBUq1GFNhO5YGmnpmaOdocjhj3FiTj5FZAztYZCsAUeDBk7CZCeWjCDbwzmURyFSwddN5LXnS3ux7aY9a9Ms53sZAZACvI3258tA0gZDZD"

def resetNlp():
  NLP = Nlp()
  NLP.reset()
  NLP.train()

""" Just home route """
@app.route('/')
def hello():
  return 'Hello World, do you like trains ?'

""" Init chatbot, IA, and others stuff """
@app.route('/init', methods=['GET'])
def init_entry():
  # Create redis queue
  q = Queue(connection=conn)

  # Queue reset nlp
  q.enqueue(resetNlp(), result_ttl=0, job_timeout=3600)

  return 'Chatbot initialized !'

""" Webhook for facebook chatbot """
@app.route('/webhook', methods=['GET', 'POST'])
def main_entry():
  # Verify token webhook to discuss with the chatbot
  if request.method == 'GET': 
    # Parse the query params
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    # Checks if a token and mode is in the query string of the request
    if mode and token:
      # Checks the mode and token sent is correct
      if mode == 'subscribe' and token == VERIFY_TOKEN:
        # Responds with the challenge token from the request
        print('WEBHOOK_VERIFIED')
        return challenge
      else:
        # Responds with '403 Forbidden' if verify tokens do not match
        abort(403)

  # We can talk to the chatbot
  elif request.method == 'POST':
    data = request.get_json(force=True)
    ts = time.time()
    voice_result = None
    path_result = None
    city_start = None
    city_end = None

    # Checks this is an event from a page subscription
    if data['object'] == 'page':
      # Iterates over each entry - there may be multiple if batched
      for entry in data['entry']:
        payload = None
        # Gets the message. entry.messaging is an array, but will only ever contain one message, so we get index 0
        webhook_data = entry['messaging'][0]
        recipient_id = webhook_data['sender']['id']
        print(webhook_data)
        print(recipient_id)

        # Get started
        if 'postback' in webhook_data and webhook_data['postback']['payload'] == 'GET_STARTED':
          # Send a text messagee explaining the chatbot
          payload_get_started = {
            "recipient": {
              "id": recipient_id
            },
            "message": {
              "text": "Bienvenue sur ce magnifique chatbot !\nIl permet de trouver les trains les plus rapides entre 2 villes.\nAttention, il ne comprend que les messages audios.\nPour commencer à l'utiliser, envoyez un message, comme par exemple : 'Je veux aller de Paris jusqu'à Montpellier.'"
            }
          }
          response = requests.post('https://graph.facebook.com/v2.6/me/messages?access_token={0}'.format(ACCESS_TOKEN), json=payload_get_started)

        elif 'message' in webhook_data:
          if 'is_echo' not in webhook_data['message'] and 'attachments' in webhook_data['message']:
            attachment = webhook_data['message']['attachments'][0]
            attachment_payload = attachment['payload']
            
            if attachment['type'] == 'audio':
              url = attachment_payload['url']
              print('audio')
              # download audio and store it in temporary file
              audio_file = requests.get(url)
              open('./tmp-{0}.mp4'.format(ts), 'wb').write(audio_file.content)

              # Use voice processing to transform to texts
              VP = VoiceProcessing()
              try:
		            # Usecase: handling from a microphone
	              # resultFromVoice = voice_process.from_audio()
		            # Usecase: handling from an audiofile
	              voice_result = VP.from_file(pathfile='./tmp-{0}.mp4'.format(ts))
              except sr.RequestError as e:
                # Send a message asking user to send an other file audio
                payload_error = {
                  "recipient": {
                    "id": recipient_id
                  },
                  "message": {
                    "text": "Problème de connexion, merci de réessayer plus tard.",
                  }
                }
                requests.post('https://graph.facebook.com/v2.6/me/messages?access_token={0}'.format(ACCESS_TOKEN), json=payload_error)
              except sr.UnknownValueError as e:
                # Send a message asking user to send an other file audio
                payload_error = {
                  "recipient": {
                    "id": recipient_id
                  },
                  "message": {
                    "text": "Message audio incompréhensible, merci de reformuler votre requête.",
                  }
                }
                requests.post('https://graph.facebook.com/v2.6/me/messages?access_token={0}'.format(ACCESS_TOKEN), json=payload_error)
              else:
                # Use nlp processing to get start and finish
                NLP = Nlp()
                # NLP.train()

                try:
                  city_start, city_finish = NLP.predict(voice_result)
                except Exception as identifier:
                  # Send a message asking user to send an other file audio
                  payload_error = {
                    "recipient": {
                      "id": recipient_id
                    },
                    "message": {
                      "text": "Désolé, mais nous n'avons trouvé aucune correspondance pour les villes {0} et {1}, merci de recommencer avec un message audio plus précis.".format(city_start, city_finish)
                    }
                  }
                  requests.post('https://graph.facebook.com/v2.6/me/messages?access_token={0}'.format(ACCESS_TOKEN), json=payload_error)
                else:
                  # Use pathfinding processing to get the best path
                  PFP = PathFinder()
                  path_result = PFP.find_path_networkx(city_start, city_end)
                  print(path_result)
                  # Create the payload
                  payload = {
                    "recipient": {
                      "id": recipient_id
                    }, 
                    "message": {
                      "attachment": {
                        "type": "template",
                        "payload": {
                          "template_type": "generic",
                          "elements":[
                            {
                              "title":"Paris -> Lyon",
                              "subtitle":"180 minutes",
                            },
                            {
                              "title":"Lyon -> Aix-en-provence",
                              "subtitle":"130 minutes",
                            },
                            {
                              "title":"Aix-en-provence -> Montpellier",
                              "subtitle":"80 minutes",
                            }
                          ]
                        }
                      }
                    }
                  }

                  # Send the result as a list template message 
                  response = requests.post('https://graph.facebook.com/v2.6/me/messages?access_token={0}'.format(ACCESS_TOKEN), json=payload)
                  # print(response.json())
                finally:
                  pass
              finally:
                # Delete the tmp audio file
                os.remove('./tmp-{0}.mp4'.format(ts))
                
      # Returns a '200 OK' response to all requests
      return 'EVENT_RECEIVED'
    else:
      # Returns a '404 Not Found' if event is not from a page subscription
      abort(404)



""" Main program """
def main():

	voice_process = VoiceProcessing()
	# A remplacer avec la récupéation du model
	NLP = Nlp()
	# NLP.reset()
	# NLP.train()
	# examples(NLP)

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

# if __name__ == "__main__":
#     main()
