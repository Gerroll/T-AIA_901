# T-AIA_901
Voice recognition to return the optimal train route between two destination

## Launch the web app in dev mode
`export FLASK_ENV=development`

`flask run`

## Launch app
`python app.py`

## Launch test
`python test.py`

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