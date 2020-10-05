from naturalLanguageProcessing import Nlp
from pathFindingProcessing import PathFinder
from voiceProcessing import VoiceProcessing

# Flask
from flask import Flask
from flask import request
from flask import abort
app = Flask(__name__)

""" Just home route """
@app.route('/')
def hello():
  return 'Hello World, do you like trains ?'

""" Webhook for facebook chatbot """
@app.route('/webhook', methods=['GET', 'POST'])
def main_entry():
  # Verify token webhook to discuss with the chatbot
  if request.method == 'GET': 
    # Your verify token. Should be a random string.
    VERIFY_TOKEN = "EAAwCqdXoSnYBANZCKxZAZAp7Xu4bwwJ6ZCUSIEa7gHvQt55oDielASlZB6ipIwdZCsNTkysCK3eYZCZCZAnowwRXz2twu4RTo1yWvfm77cGsGu6XMlAgXtN89Nerqg5iQhUiLq54DxP4j57xOY3BqNlzchEzeP740wAP8IhROfhLyXwZDZD"
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
    print(data)
    # Checks this is an event from a page subscription
    if data['object'] == 'page':
      # Iterates over each entry - there may be multiple if batched
      for entry in data['entry']:
        # Gets the message. entry.messaging is an array, but will only ever contain one message, so we get index 0
        webhook_event = entry['messaging'][0]
        print(webhook_event)

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
