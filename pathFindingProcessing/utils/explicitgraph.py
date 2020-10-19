from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt


class ExplicitGraph:
	def __init__(self, matrix_graph, town):
		self.matrix_graph = matrix_graph
		self.town = town

	@staticmethod
	def min_distance(dist, queue):
		minimum = float("Inf")
		min_index = -1

		for i in range(len(dist)):
			if dist[i] < minimum and i in queue:
				minimum = dist[i]
				min_index = i
		return min_index

	def print_path(self, parent, j):
		if parent[j] == -1:
			print(j)
			return
		self.print_path(parent, parent[j])
		print(j)

	def build_path(self, parent, j, target, previous):
		if parent[j] == -1:
			depart = self.town[j]
			arrive = self.town[previous]
			target["duration"][depart + "->" + arrive] = self.matrix_graph[previous][j]
			target["path"].append(depart)
			return
		self.build_path(parent, parent[j], target, j)
		depart = self.town[j]
		if previous is not None:
			arrive = self.town[previous]
			target["duration"][depart + "->" + arrive] = self.matrix_graph[previous][j]
		target["path"].append(depart)

	def print_solution(self, src, dist, parent):
		print("Vertex \t\tDistance from Source\tPath")
		for i in range(len(dist)):
			if dist[i] == float("Inf"):
				continue
			print("\n%d --> %d \t\t%d \t\t\t\t\t" % (src, i, dist[i])),
			self.print_path(parent, i)

	def build_solution(self, arrive, dist, parent):
		target = {
			'min': dist[arrive],
			'path': [],
			'duration': {}
		}
		if dist[arrive] == float("Inf"):
			return target
		self.build_path(parent, arrive, target, None)
		return target

	def draw(self):
		h: int = len(self.matrix_graph)
		w: int = len(self.matrix_graph[0])

		# build networkx graph from matrix
		nwxGraph: nx.Graph = nx.Graph()
		## Add node
		for t in self.town:
			nwxGraph.add_node(t)
		## Add edge
		for j in range(h):
			for i in range(w):
				if self.matrix_graph[j][i] != 0:
					nwxGraph.add_edge(self.town[i], self.town[j])

		options = {
			'node_color': 'red',
			'node_size': 10,
			'width': 3,
			'with_labels': True,
			'font_weight': 'bold',
			'font_color': 'blue',
		}
		print(nwxGraph.edges)
		nx.draw(nwxGraph, **options)

		plt.show()

	def dijkstra(self, depart, arrive):
		row = len(self.matrix_graph)
		col = len(self.matrix_graph[0])

		# The output array. dist[i] will hold
		# the shortest distance from src to i
		# Initialize all distances as INFINITE
		dist = [float("Inf")] * row

		# Parent array to store
		# shortest path tree
		parent = [-1] * row

		# Distance of source vertex
		# from itself is always 0
		dist[depart] = 0

		# Add all vertices in queue
		queue = list(range(row))
		previous = -2
		while queue:
			u = ExplicitGraph.min_distance(dist, queue)
			if u == previous:
				break
			if u in queue:
				queue.remove(u)
			for i in range(col):
				if self.matrix_graph[u][i] and i in queue:
					if dist[u] + self.matrix_graph[u][i] < dist[i]:
						dist[i] = dist[u] + self.matrix_graph[u][i]
						parent[i] = u
			previous = u

		return self.build_solution(arrive, dist, parent)


if __name__ == "__main__":
	graph = [[0, 4, 0, 0, 0, 0, 0, 8, 0],
			[4, 0, 8, 0, 0, 0, 0, 11, 0],
			[0, 8, 0, 7, 0, 4, 0, 0, 2],
			[0, 0, 7, 0, 9, 14, 0, 0, 0],
			[0, 0, 0, 9, 0, 10, 0, 0, 0],
			[0, 0, 4, 14, 10, 0, 2, 0, 0],
			[0, 0, 0, 0, 0, 2, 0, 1, 6],
			[8, 11, 0, 0, 0, 0, 1, 0, 7],
			[0, 0, 2, 0, 0, 0, 6, 7, 0]]

	graph_non_connexe = [[0, 4, 0, 0, 0, 0, 0, 0, 0],
						[4, 0, 8, 0, 0, 0, 0, 0, 0],
						[0, 8, 0, 7, 0, 4, 0, 0, 2],
						[0, 0, 7, 0, 9, 14, 0, 0, 0],
						[0, 0, 0, 9, 0, 10, 0, 0, 0],
						[0, 0, 4, 14, 10, 0, 2, 0, 0],
						[0, 0, 0, 0, 0, 2, 0, 1, 6],
						[0, 0, 0, 0, 0, 0, 1, 0, 7],
						[0, 0, 2, 0, 0, 0, 6, 7, 0]]

	town = ["Paris", "Berlin", "Toronto", "San Francisco", "Downtown", "Berk", "Montpellier", "Munich", "Tokyo"]
	g = ExplicitGraph(graph, town)
	print(g.dijkstra(4, 7))
	g.draw()
