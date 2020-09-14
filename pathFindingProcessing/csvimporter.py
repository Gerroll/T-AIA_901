import csv
import networkx as nx
import matplotlib.pyplot as plt

class CSVImporter:

    def __init__(self):
        self.data = []
        self.ordered_town = []
        self.graph = []
        self.tot = nx.Graph()

    def open(self, path):
        with open(path, newline='') as f:
            reader = csv.reader(f)
            raw_data = list(reader)
            self.extract_data(raw_data)

    def get_data(self):
        return self.data

    def extract_data(self, data):
        for row in data:
            if data.index(row) == 0: continue
            if len(row) >= 2: continue
            format_row = []
            fc = row[0]
            lr = fc.split('\t')
            format_row.append(lr[0])
            trajet = lr[1].split(' - ')
            if len(trajet) >= 3:
                print("WARNING: Malformed trajet: " + lr[1])
            else:
                depart = trajet[0]
                arrive = trajet[1]
                if depart not in self.ordered_town:
                    self.ordered_town.append(depart)
                    self.tot.add_node(depart)
                if arrive not in self.ordered_town:
                    self.ordered_town.append(arrive)
                    self.tot.add_node(arrive)
                format_row.append(depart)
                format_row.append(arrive)
                self.tot.add_edge(depart, arrive)
                format_row.append(lr[2])
                self.data.append(format_row)

    def build_graph(self):
        lot = len(self.ordered_town)
        graph = [[0 for column in range(lot)] for row in range(lot)]

        for row in self.data:
            depart = row[1]
            arrive = row[2]
            distance = row[3]
            index_of_depart = self.ordered_town.index(depart)
            index_of_arrive = self.ordered_town.index(arrive)

            graph[index_of_depart][index_of_arrive] = int(distance)
            graph[index_of_arrive][index_of_depart] = int(distance)

        return graph


if __name__ == "__main__":
    ci = CSVImporter()
    ci.open('../data/timetables.csv')
    graph = ci.build_graph()

    nx.draw(ci.tot)
    plt.draw()
    plt.show()


