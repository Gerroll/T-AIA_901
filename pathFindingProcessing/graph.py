from collections import defaultdict


class Graph:
	def __init__(self, matrix_graph, town):
		self.matrix_graph = matrix_graph
		self.town = town

	def minDistance(self, dist, queue):
		minimum = float("Inf")
		min_index = -1

		for i in range(len(dist)):
			if dist[i] < minimum and i in queue:
				minimum = dist[i]
				min_index = i
		return min_index

	def printPath(self, parent, j):
		if parent[j] == -1:
			print(j)
			return
		self.printPath(parent, parent[j])
		print(j)

	def buildPath(self, parent, j, target, previous):
		if parent[j] == -1:
			depart = self.town[j]
			arrive = self.town[previous]
			target["duration"][depart + "->" + arrive] = self.matrix_graph[previous][j]
			target["path"].append(depart)
			return
		self.buildPath(parent, parent[j], target, j)
		depart = self.town[j]
		if previous is not None:
			arrive = self.town[previous]
			target["duration"][depart + "->" + arrive] = self.matrix_graph[previous][j]
		target["path"].append(depart)

	def printSolution(self, src, dist, parent):
		print("Vertex \t\tDistance from Source\tPath")
		for i in range(len(dist)):
			if dist[i] == float("Inf"):
				continue
			print("\n%d --> %d \t\t%d \t\t\t\t\t" % (src, i, dist[i])),
			self.printPath(parent, i)

	def buildSolution(self, arrive, dist, parent):
		target = {
			'min': dist[arrive],
			'path': [],
			'duration': {}
		}
		if dist[arrive] == float("Inf"):
			return target
		self.buildPath(parent, arrive, target, None)
		return target

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
		# Find shortest path for all vertices
		while queue:

			# Pick the minimum dist vertex
			# from the set of vertices
			# still in queue
			u = self.minDistance(dist, queue)
			if u == previous:
				break
			# remove min element
			if u in queue:
				queue.remove(u)
			# Update dist value and parent
			# index of the adjacent vertices of
			# the picked vertex. Consider only
			# those vertices which are still in
			# queue
			for i in range(col):
				'''Update dist[i] only if it is in queue, there is 
				an edge from u to i, and total weight of path from 
				src to i through u is smaller than current value of 
				dist[i]'''
				if self.matrix_graph[u][i] and i in queue:
					if dist[u] + self.matrix_graph[u][i] < dist[i]:
						dist[i] = dist[u] + self.matrix_graph[u][i]
						parent[i] = u
			previous = u

		# print the constructed distance array
		#self.printSolution(depart, dist, parent)
		return self.buildSolution(arrive, dist, parent)


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

	town = ["Paris", "Berlin", "Toronto", "San Francisco", "Downtown", "Berk", "Viol-le-fort", "Munich", "Tokyo"]
	g = Graph(graph, town)
	# Print the solution
	print(g.dijkstra(4, 7))
