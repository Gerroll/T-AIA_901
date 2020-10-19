from pathFindingProcessing.utils import StationParser
from pathFindingProcessing.utils import StationMapping
from pathFindingProcessing.utils import NetworkxGraph


class PathFinder:
	def __init__(self):
		parser = StationParser()
		self.matrix_graph = parser.get_matrix_graph()
		self.raw_data = parser.get_data()
		self.stations = parser.get_stations()
		self.networkxG = NetworkxGraph(self.raw_data)

	def find_path_networkx(self, depart: str, arrive: str):
		lowDep: str = depart.lower()
		lowArr: str = arrive.lower()

		sm: StationMapping = StationMapping()
		depart_station: list = sm.get_stations_from_unidentified(lowDep)
		arrive_station: list = sm.get_stations_from_unidentified(lowArr)

		# compute all trajectory
		traj = []
		for dep in depart_station:
			for arri in arrive_station:
				if dep in self.stations and arri in self.stations:
					traj.append(self.networkxG.dijkstra(dep, arri))

		# find min trajectory
		result = None
		minimum = float('Inf')
		for t in traj:
			if t['min'] < minimum:
				result = t
				minimum = t['min']
		return result


if __name__ == "__main__":
	pf = PathFinder()
	print(pf.find_path_networkx("gare de paris-est", "vosges"))
