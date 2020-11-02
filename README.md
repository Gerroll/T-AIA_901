# T-AIA_901
Voice recognition to return the optimal train route between two destination

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

## Test module pathFindingProcessing
From app.py
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
