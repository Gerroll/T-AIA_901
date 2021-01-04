import requests
from flask import request
from flask import abort
from worker import conn

import os
import time

# Verify token. Should be a random string.
VERIFY_TOKEN = "EAAwCqdXoSnYBANZCKxZAZAp7Xu4bwwJ6ZCUSIEa7gHvQt55oDielASlZB6ipIwdZCsNTkysCK3eYZCZCZAnowwRXz2twu4RTo1yWvfm77cGsGu6XMlAgXtN89Nerqg5iQhUiLq54DxP4j57xOY3BqNlzchEzeP740wAP8IhROfhLyXwZDZD"
ACCESS_TOKEN = "EAAwCqdXoSnYBANPAkd3tEJqSLjFFKgcg9sGkvZA9dgpGjWBGpmZA4HaEUC8SO8qg0CIObN5qjEELTj8IrZArG4aqRxZBw0X47935hNwCscgDCH5oNpM3mrVBTqaI8ZCGS2UJ3ziFDXjDNoWR9TZAScupTE65b27gjKqaMCi9Wn0wZDZD"

class Chatbot:
  def __init__(self, voiceModule, nlpModule, pathModule):
    self.facebook_url = f'https://graph.facebook.com/v8.0/me/messages?access_token={ACCESS_TOKEN}'
    
    self.voiceModule = voiceModule
    self.nlpModule = nlpModule
    self.pathModule = pathModule

    self.flow = 0
    self.audio_received = False
    self.user = None


  def dispatch_request(self, request):
    if request.method == 'GET':
      return self.process_get_request(request)
    elif request.method == 'POST':
      return self.process_post_request(request)
  
  def process_post_request(self, request):
    data = request.get_json(force=True)
    ts = time.time()
    pathfile = os.path.basename(f'./tmp-{ts}')
    voice_result = None
    path_result = None
    city_start = None
    city_end = None

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
          # Set redis user
          self.user = recipient_id
          # Send a text messagee explaining the chatbot
          self.send_text_payload("Bienvenue sur ce magnifique chatbot !\nIl permet de trouver les trains les plus rapides entre 2 villes.\nAttention, il ne comprend que les messages audios.\nPour commencer à l'utiliser, envoyez un message, comme par exemple : 'Je veux aller de Paris jusqu'à Montpellier.'")

        elif 'message' in webhook_data and 'is_echo' not in webhook_data and conn.get('audio_received') == b'false' and int(self.flow) == 0: # is_echo means its sended by the page itself
          if 'is_echo' not in webhook_data['message'] and 'attachments' in webhook_data['message']:
            attachment = webhook_data['message']['attachments'][0]
            attachment_payload = attachment['payload']
            
            if attachment['type'] == 'audio':
              print('Received audio from client on chatbot')
              self.audio_received = True
              # Set redis user flow variable
              self.flow = 1

              url = attachment_payload['url']
              # download audio and store it in temporary file
              audio_file = requests.get(url)
              open(pathfile + '.mp4', 'wb').write(audio_file.content)

              try:
                print('Start voice processing')
                # Usecase: handling from an audiofile
                voice_result = self.voiceModule.from_file(pathfile=pathfile)
                print('Voice result :', voice_result)

              except sr.RequestError as e:
                self.flow = 0
                self.audio_received = False
                # Send a message asking user to send an other file audio
                self.send_text_payload(
                  self.user,
                  "Problème de connexion, merci de réessayer plus tard."
                )

              except sr.UnknownValueError as e:
                self.flow = 0
                self.audio_received = False
                # Send a message asking user to send an other file audio
                self.send_text_payload(
                  self.user,
                  "Message audio incompréhensible, merci de reformuler votre requête."
                )

              else:
                # Set redis user flow variable
                self.flow = 2

                try:
                  print('Start natural language processing')
                  # (city_start, city_end) = NLP.predict(voice_result)
                  (city_start, city_end) = self.nlpModule.predict(voice_result)
                  print(f'city start: {city_start}')
                  print(f'city end: {city_end}')

                except Exception as identifier:
                  self.flow = 0
                  self.audio_received = False
                  # Send a message asking user to send an other file audio
                  self.send_text_payload(f"Désolé, mais nous n'avons trouvé aucune correspondance pour les villes {city_start} et {city_end}, merci de recommencer avec un message audio plus précis.")

                else:
                  # Set redis user flow variable
                  self.flow = 3

                  try:
                    print('Start pathfinding')
                    if city_start and city_end:
                      # Use pathfinding processing to get the best path
                      path_result = self.pathModule.find_path_networkx(city_start, city_end)
                      print('Path result : {}'.format(path_result))

                  except Exception as e:
                    self.flow = 0
                    self.audio_received = False
                    print('error : {}'.format(e))
                    
                  else:
                    if path_result:
                      stops = path_result['stops']
                      # Send a resume template with main informations
                      stop_start = stops[0].swapcase()
                      stop_end = stops[len(stops) - 1].swapcase()
                      element = [
                        {
                          'title': 'Trajet de {} à {}'.format(city_start, city_end),
                          'subtitle': 'Temps total de {} minutes'.format(path_result['min'])
                        }
                      ]
                      self.send_generic_payload(element)

                      # Create the payload for the path response
                      elements = []

                      for item in path_result['path']:
                        elements.append({
                          'title': '{} -> {}'.format(item['start'].swapcase(), item['end'].swapcase()),
                          'subtitle': '{} minutes'.format(item['duration'])
                        })
                      self.send_generic_payload(elements)

              finally:
                voice_result = None
                path_result = None
                city_start = None
                city_end = None
                self.flow = 0
                self.audio_received = False
                # Delete the tmp audio file
                os.remove(pathfile + '.mp4')

                
          elif 'is_echo' not in webhook_data['message'] and 'text' in webhook_data['message']: # the user send a text message
            # Send a message asking user to send an other file audio
            self.send_text_payload(f"Désolé, mais ce chatbot ne traite que les messages audios. Merci de recommencer.")

        # break the loop
        break

      # Returns a '200 OK' response to all requests
      return ('POST', 'EVENT_RECEIVED', 200)

    else:
      # Returns a '404 Not Found' if event is not from a page subscription
      return ('POST', None, 404)

  def process_get_request(self, request):
    # Verify token webhook to discuss with the chatbot
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
        return ('GET', challenge, 200)
      else:
        # Responds with '403 Forbidden' if verify tokens do not match
        return ('GET', None, 403)


  def send_text_payload(self, message=None):
    if self.user and message:
      payload = {
        "recipient": {
          "id": self.user
        },
        "message": {
          "text": message,
        }
      }
      requests.post(self.facebook_url, json=payload)
  
  def send_generic_payload(self, elements=None):
    if self.user and elements and len(elements) > 0:
      payload = {
        "recipient": {
          "id": self.user
        }, 
        "message": {
          "attachment": {
            "type": "template",
            "payload": {
              "template_type": "generic",
              "elements": elements
            }
          }
        }
      }
      requests.post(self.facebook_url, json=payload)

