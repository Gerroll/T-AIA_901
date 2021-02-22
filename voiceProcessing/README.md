# T-AIA_901
Voice recognition to return the optimal train route between two destination

## Voice Recognition
A utiliser sans venv.

`pip install SpeechRecognition PyAudio`

On instancie la classe dans app.py
    
`voice_process = VoiceProcessing()`

Les fonctions retournent une chaine de caractères de mots francais correspondant a ce qui à été entendu.
La ponctuation est généralement absente.
En cas d'erreur, un message s'affiche sur la console et les fonctions retournent une chaine de caractères vide.

#### Depuis un micro
Un micro doit etre a disposition sur votre pc (micro par default).

`result = voice_process.from_audio()`
Le fichier enregistre pendant 10s max et s'arrète si on ne parle pas de quelques secondes.

#### Depuis un fichier sonore 

`result = voice_process.from_file(pathfile="chemin_du_fichier.flac")`
Le chemin doit être fourni relativement au fichier app.py

Formats acceptés: 
- WAV: must be in PCM/LPCM format
- AIFF
- AIFF-C
- FLAC: must be native FLAC format; OGG-FLAC is not supported