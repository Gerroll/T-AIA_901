import networkx as nx
import matplotlib.pyplot as plt


class NetworkxGraph:
    def __init__(self, data):
        self.graph: nx.Graph = nx.Graph()
        for row in data:
            depart: str = row[0]
            arrive: str = row[1]
            distance: int = row[2]
            self.graph.add_edge(depart, arrive, distance=distance)

    def dijkstra(self, depart: str, arrive: str):
        length: int = nx.dijkstra_path_length(self.graph, depart, arrive, 'distance')
        path: list = nx.dijkstra_path(self.graph, depart, arrive, 'distance')
        target = {
            'min': length,
            'path': path,
            'duration': self.build_duration(path)
        }
        return target

    def build_duration(self, path):
        target = []

        if len(path) <= 1:
            raise Exception("path doesn't contains enough data")
        for i in range(0, len(path) - 1):
            target.append({
                'start': path[i],
                'end': path[i + 1],
                'duration': self.graph.edges[path[i], path[i + 1]]['distance']
            })
        return target

    def draw(self):
        options = {
            'node_color': 'red',
            'node_size': 10,
            'width': 3,
            'with_labels': True,
            'font_weight': 'bold',
            'font_color': 'blue',
        }
        print(self.graph.edges)
        nx.draw(self.graph, **options)

        plt.show()


def main():
    # liste des départs/arrivées avec leur distance associée
    raw_data = [['Paris', 'Berlin', 4], ['Paris', 'Munich', 8], ['Berlin', 'Toronto', 8], ['Berlin', 'Munich', 11],
                ['Toronto', 'San Francisco', 7], ['Toronto', 'Berk', 4], ['Toronto', 'Tokyo', 2],
                ['San Francisco', 'Downtown', 9], ['San Francisco', 'Berk', 14], ['Downtown', 'Berk', 10],
                ['Berk', 'Montpellier', 2], ['Montpellier', 'Munich', 1], ['Montpellier', 'Tokyo', 6],
                ['Munich', 'Tokyo', 7]]

    g = NetworkxGraph(raw_data)
    print(g.dijkstra("Downtown", "Munich"))
    g.draw()
