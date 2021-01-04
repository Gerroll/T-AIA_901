import requests
from flask import request
from flask import abort

import os
import time


class MainController:
  def __init__(self, voiceModule, nlpModule, pathModule):

    self.voiceModule = voiceModule
    self.nlpModule = nlpModule
    self.pathModule = pathModule

    self.flow = 0
    self.audio_received = False
    self.user = None
  
  def process_post_request(self, request):
    data = request.get_json(force=True)
    ts = time.time()
    pathfile = os.path.basename(f'./tmp-{ts}')
    voice_result = None
    path_result = None
    city_start = None
    city_end = None

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
      # self.send_text_payload(
      #   self.user,
      #   "Problème de connexion, merci de réessayer plus tard."
      # )

    except sr.UnknownValueError as e:
      self.flow = 0
      self.audio_received = False
      # Send a message asking user to send an other file audio
      # self.send_text_payload(
      #   self.user,
      #   "Message audio incompréhensible, merci de reformuler votre requête."
      # )

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
        # self.send_text_payload(f"Désolé, mais nous n'avons trouvé aucune correspondance pour les villes {city_start} et {city_end}, merci de recommencer avec un message audio plus précis.")

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
            # element = [
            #   {
            #     'title': 'Trajet de {} à {}'.format(city_start, city_end),
            #     'subtitle': 'Temps total de {} minutes'.format(path_result['min'])
            #   }
            # ]
            # self.send_generic_payload(element)

            # Create the payload for the path response
            # elements = []

            # for item in path_result['path']:
            #   elements.append({
            #     'title': '{} -> {}'.format(item['start'].swapcase(), item['end'].swapcase()),
            #     'subtitle': '{} minutes'.format(item['duration'])
            #   })
            # self.send_generic_payload(elements)

        finally:
          voice_result = None
          path_result = None
          city_start = None
          city_end = None
          self.flow = 0
          self.audio_received = False
          # Delete the tmp audio file
          os.remove(pathfile + '.mp4')

    # Returns a '200 OK' response to all requests
    return ('POST', 'EVENT_RECEIVED', 200)

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

