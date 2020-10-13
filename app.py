from naturalLanguageProcessing import Nlp
from pathFindingProcessing import PathFinder
from voiceProcessing import VoiceProcessing

# Flask
from flask import Flask
from flask import request
from flask import abort
import requests
import os
import time
app = Flask(__name__)

# Verify token. Should be a random string.
VERIFY_TOKEN = "EAAwCqdXoSnYBANZCKxZAZAp7Xu4bwwJ6ZCUSIEa7gHvQt55oDielASlZB6ipIwdZCsNTkysCK3eYZCZCZAnowwRXz2twu4RTo1yWvfm77cGsGu6XMlAgXtN89Nerqg5iQhUiLq54DxP4j57xOY3BqNlzchEzeP740wAP8IhROfhLyXwZDZD"
ACCESS_TOKEN = "EAAwCqdXoSnYBAGvZAVkROulrJLGagS2DgeAo2SaHMlbZAvZAOflFgm1TuzR2QeWhmJt6OpbQZBBUq1GFNhO5YGmnpmaOdocjhj3FiTj5FZAztYZCsAUeDBk7CZCeWjCDbwzmURyFSwddN5LXnS3ux7aY9a9Ms53sZAZACvI3258tA0gZDZD"

""" Just home route """
@app.route('/')
def hello():
  return 'Hello World, do you like trains ?'

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
    print(data)
    # Checks this is an event from a page subscription
    if data['object'] == 'page':
      # Iterates over each entry - there may be multiple if batched
      for entry in data['entry']:
        # Gets the message. entry.messaging is an array, but will only ever contain one message, so we get index 0
        webhook_data = entry['messaging'][0]
        recipient_id = webhook_data['sender']['id']
        print(webhook_data)
        print(recipient_id)

        # Get started
        if 'postback' in webhook_data and webhook_data['postback']['payload'] == 'GET_STARTED':
          print('get started')
          # Send a text messagee explaining the chatbot
          payload = {
            "messaging_type": "RESPONSE",
            "recipient": {
              "id": recipient_id
            },
            "message": {
              "text": "Bienvenue sur ce magnifique chatbot !\nIl permet de trouver les trains les plus rapides entre 2 villes.\nAttention, il nee comprend que les messages audios.\nPour commencer à l'utiliser, envoyez un message, comme par exemple : 'Je veux aller de Paris jusqu'à Montpellier.'"
            }
          }
          response = requests.post('https://graph.facebook.com/v8.0/me/messages?access_token={0}'.format(ACCESS_TOKEN), data=payload)
          print(response.json())

        if 'message' in webhook_data:
          print('webhook')
          if 'attachments' in webhook_data['message']:
            print('attachment')
            attachment = webhook_data['message']['attachments'][0]
            attachment_payload = attachment['payload']
            url = attachment_payload['url']
            
            if attachment['type'] == 'audio':
              print('audio')
              # download audio and store it in temporary file
              audio_file = requests.get(url)
              open('./tmp-{0}.mp4'.format(ts), 'wb').write(audio_file.content)

              # Use voice processing to transform to texts

              # Use nlp processing to get start and finish

              # Use pathfinding processing to get the best path

              # Delete the tmp audio file
              os.remove('./tmp-{0}.mp4'.format(ts))

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
                          "title":"Welcome!",
                          "subtitle":"We have the right hat for everyone.",
                        }
                      ]
                    }
                  }
                }
              }

              # Send the result as a list template message 
              response = requests.post('https://graph.facebook.com/v8.0/me/messages?access_token={0}'.format(ACCESS_TOKEN), data=payload)

              print(response.json())

      # Returns a '200 OK' response to all requests
      return 'EVENT_RECEIVED'
    else:
      # Returns a '404 Not Found' if event is not from a page subscription
      abort(404)



""" Main program """
def main():
	print('Hello world !')
	NLP = Nlp()
	NLP.train()

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
