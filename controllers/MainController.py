import requests
from flask import request
from flask import abort
import speech_recognition as sr

import os
import time


class MainController:
  def __init__(self, voiceModule, nlpModule, pathModule):

    self.voiceModule = voiceModule
    self.nlpModule = nlpModule
    self.pathModule = pathModule

    self.flow = 0
    self.audio_received = False
  
  def process_audio(self, data):
    ts = time.time()
    pathfile = os.path.basename(f'./tmp-{ts}')
    voice_result = None
    path_result = None
    city_start = None
    city_end = None
    result = {
      'start': None,
      'end': None,
      'total': None,
      'path': []
    }

    # download audio and store it in file
    with open(pathfile + '.mp3', 'wb+') as f:
        for chunk in data: 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

    try:
      print('Start voice processing')
      # Usecase: handling from an audiofile
      voice_result = self.voiceModule.from_file(pathfile)
      print('Voice result :', voice_result)

    except sr.RequestError as e:
      self.flow = 0
      self.audio_received = False
      return ("Problème de connexion, merci de réessayer plus tard.", 666)


    except sr.UnknownValueError as e:
      self.flow = 0
      self.audio_received = False
      return ("Message audio incompréhensible, merci de reformuler votre requête.", 666)

    else:
      self.flow = 2

      try:
        print('Start natural language processing')
        (city_start, city_end) = self.nlpModule.predict(voice_result)
        print(f'city start: {city_start}')
        print(f'city end: {city_end}')

      except Exception as identifier:
        self.flow = 0
        self.audio_received = False
        return (f"Désolé, mais nous n'avons trouvé aucune correspondance pour les villes {city_start} et {city_end}, merci de recommencer avec un message audio plus précis.", 666)

      else:
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
          return (e, 666)
          
        else:
          if path_result:
            # Send a resume template with main informations
            result['start'] = city_start
            result['end'] = city_end
            result['total'] = path_result['min']

            # Create the payload for the path response
            for item in path_result['path']:
              result['path'].append({
                'start': item['start'].swapcase(),
                'stop': item['end'].swapcase(),
                'duration': item['duration']
              })

        finally:
          voice_result = None
          path_result = None
          city_start = None
          city_end = None
          self.flow = 0
          self.audio_received = False
          # Delete the tmp audio file
          os.remove(pathfile + '.mp3')

    # Returns a '200 OK' response to all requests
    return (result, 200)

