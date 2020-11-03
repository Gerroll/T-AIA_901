# T-AIA_901
Voice recognition to return the optimal train route between two destination


##Voice Recognition 
A utiliser sans venv 

    pip install SpeechRecognition PyAudio
On instancie la classe dans app.py
    
    voice_process = VoiceProcessing()
Les fonctions retournent une chaine de caractères de mots francais correspondant a ce qui à été entendu.
La ponctuation est généralement absente. 
En cas d'erreur, un message s'affiche sur la console et les fonctions retournent une chaine de caractères vide 
#### Depuis un micro
Un micro doit etre a disposition sur votre pc (micro par default)

      result = voice_process.from_audio()   
Le fichier enregistre pendant 10s max et s'arrète si on ne parle pas de quelques secondes
####Depuis un fichier sonore 

      result = voice_process.from_file(pathfile="chemin_du_fichier.flac")
Le chemin doit être fourni relativement au fichier app.py

Formats acceptés: 
- WAV: must be in PCM/LPCM format
- AIFF
- AIFF-C
- FLAC: must be native FLAC format; OGG-FLAC is not supported
## Using Virtualenv
### Install virtual env
`pip install virtualenv`

### Init virtualenv
`virtualenv -p python3.7 venv3.7`

### Use existing virtualenv
Ubuntu : 
`source venv3.7/bin/activate`

Windows: 
`venv3.7\Scripts\activate.bat`

### Install package in virtualenv
`pip install <module>`

### Save dependencies
`pip freeze > requirements3.7.txt`

### Load dependencies
`pip install -r requirements3.7.txt`

### Stop using virtualenv
`deactivate`

## Using [Pipenv](https://pipenv.pypa.io/en/latest/)
### Install pipenv
`pip install --user pipenv`

### Init project with python 3.7
`pipenv --python path/to/python3.7`

### Install dependencies from requirements.txt 
`pipenv install -r requirements.txt`

### Install package
`pipenv install <module>`

### Activate environnement
`pipenv shell`

### Run program
`pipenv run python3 app.py`

## Test module pathFindingProcessing
Example of use:
```
from pathFindingProcessing import PathFinder

pf = PathFinder()
result = pf.find_path_networkx("gare de paris-est", "vosges")
print(result)
```
Result expected:
```
{
  'min': 227,
  'path': [
    'gare de paris-est',
    'gare de chaumont',
    'gare de culmont-chalindrey',
    'gare de vittel'
  ],
  'duration': {
    'gare de paris-est->gare de chaumont': 145,
    'gare de chaumont->gare de culmont-chalindrey': 33,
    'gare de culmont-chalindrey->gare de vittel': 49
  }
}
```
Example of use for some functionality from app.py
- Display the list of authorized stations, cities or departments
```
import pathFindingProcessing.utils.stationmapping as map

sm = map.StationMapping()
print(sm.get_station())
print(sm.get_town())
print(sm.get_department())
```
- Test pathfinder.py
```
import pathFindingProcessing as pfp

pfp.main()
```
- Test networkxgraph.py
```
import pathFindingProcessing.utils.networkxgraph as net

net.main()
```
- Test stationmapping.py
```
import pathFindingProcessing.utils.stationmapping as map

map.main()
```
- Test stationparser.py
```
import pathFindingProcessing.utils.stationparser as par
par.main()
```
