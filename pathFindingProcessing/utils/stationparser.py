import csv
import os
from pathFindingProcessing.utils.util import Util


class StationParser:
    def __init__(self):
        self.__data = []
        self.__stations = []
        data_file = os.path.join(os.path.dirname(__file__), 'resource', 'timetables.csv')
        with open(data_file, newline='') as f:
            reader = csv.reader(f)
            raw_data = list(reader)
            self.__extract_data(raw_data)

    def __extract_data(self, data):
        for row in data:
            if data.index(row) == 0: continue
            if len(row) >= 2: continue
            format_row = []
            fc = row[0]
            lr = fc.split('\t')
            trajet: list = lr[1].split(' - ')
            if len(trajet) >= 3:
                print("WARNING: Malformed trajet: " + lr[1])

                # to lower case
                depart: str = trajet[0].lower()
                arrive: str = trajet[2].lower()

                # remove accents
                depart = Util.string_no_accents(depart)
                arrive = Util.string_no_accents(arrive)

                print("depart choisie: " + depart)
                print("arrive choisie: " + arrive)
                if depart not in self.__stations:
                    self.__stations.append(depart)
                if arrive not in self.__stations:
                    self.__stations.append(arrive)
                format_row.append(depart)
                format_row.append(arrive)
                format_row.append(int(lr[2]))
                self.__data.append(format_row)
            else:
                # to lower case
                depart: str = trajet[0].lower()
                arrive: str = trajet[1].lower()

                # remove accents
                depart = Util.string_no_accents(depart)
                arrive = Util.string_no_accents(arrive)

                if depart not in self.__stations:
                    self.__stations.append(depart)
                if arrive not in self.__stations:
                    self.__stations.append(arrive)
                format_row.append(depart)
                format_row.append(arrive)
                format_row.append(int(lr[2]))
                self.__data.append(format_row)

    def get_data(self):
        return self.__data

    def get_stations(self):
        return self.__stations

    def get_matrix_graph(self):
        lot = len(self.__stations)
        graph = [[0 for _ in range(lot)] for _ in range(lot)]

        for row in self.__data:
            depart: str = row[0]
            arrive: str = row[1]
            distance: int = row[2]
            index_of_depart = self.__stations.index(depart)
            index_of_arrive = self.__stations.index(arrive)

            graph[index_of_depart][index_of_arrive] = distance
            graph[index_of_arrive][index_of_depart] = distance

        return graph


def main():
    sp = StationParser()
    print("STATION")
    print(sp.get_stations())
