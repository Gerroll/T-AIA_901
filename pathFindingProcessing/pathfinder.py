from pathFindingProcessing.utils import StationParser
from pathFindingProcessing.utils import ExplicitGraph
from pathFindingProcessing.utils import StationMapping


class PathFinder:
	def __init__(self):
		parser = StationParser()
		self.matrix_graph = parser.get_matrix_graph()
		self.stations = parser.get_stations()
		self.expG = ExplicitGraph(self.matrix_graph, self.stations)

	def find_path_exp(self, depart: str, arrive: str):
		lowDep: str = depart.lower()
		lowArr: str = arrive.lower()

		sm: StationMapping = StationMapping()
		depart_station: list = sm.get_stations_from_unidentified(lowDep)
		arrive_station: list = sm.get_stations_from_unidentified(lowArr)

		# compute all trajectory
		traj = []
		for dep in depart_station:
			for arri in arrive_station:
				try:
					index_depart = self.stations.index(dep)
					index_arrive = self.stations.index(arri)
					traj.append(self.expG.dijkstra(index_depart, index_arrive))
				except ValueError as ex:
					pass
					#print(ex)

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
	print(pf.find_path_exp("gare de paris-est", "vosges"))
