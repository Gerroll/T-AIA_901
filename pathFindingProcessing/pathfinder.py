from csvimporter import CSVImporter
from graph import Graph


class PathFinder:
	def __init__(self):
		self.ci = CSVImporter()
		self.ci.open('../data/timetables.csv')
		self.matrix_graph = self.ci.build_graph()
		self.G = Graph(self.matrix_graph, self.ci.ordered_town)

	def find_path(self, depart, arrive):
		self.verification(arrive, depart)
		index_depart = self.ci.ordered_town.index(depart)
		index_arrive = self.ci.ordered_town.index(arrive)
		return self.G.dijkstra(index_depart, index_arrive)

	def verification(self, depart, arrive):
		if depart not in self.ci.ordered_town:
			raise Exception("Depart not found or misspelled in the current csv")
		if arrive not in self.ci.ordered_town:
			raise Exception("Arrive not found or misspelled in the current csv")

if __name__ == "__main__":
	pf = PathFinder()
	print(pf.find_path("Gare de Le Havre", "Gare de Caen"))
