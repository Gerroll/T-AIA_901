# T-AIA_901
Voice recognition to return the optimal train route between two destination

## Path Finding

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
