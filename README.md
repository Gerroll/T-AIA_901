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
