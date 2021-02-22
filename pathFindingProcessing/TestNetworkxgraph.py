import unittest
import networkx as nx
from pathFindingProcessing.utils import NetworkxGraph


class TestNetworkxgraph(unittest.TestCase):

    def test_dijsktra_1(self):
        raw_data = [['Paris', 'Berlin', 4], ['Paris', 'Munich', 8], ['Berlin', 'Toronto', 8], ['Berlin', 'Munich', 11],
                    ['Toronto', 'San Francisco', 7], ['Toronto', 'Berk', 4], ['Toronto', 'Tokyo', 2],
                    ['San Francisco', 'Downtown', 9], ['San Francisco', 'Berk', 14], ['Downtown', 'Berk', 10],
                    ['Berk', 'Montpellier', 2], ['Montpellier', 'Munich', 1], ['Montpellier', 'Tokyo', 6],
                    ['Munich', 'Tokyo', 7]]
        ng1 = NetworkxGraph(raw_data)

        result = ng1.dijkstra("Downtown", "Munich")
        expected = {'min': 13,
                    'path': ['Downtown', 'Berk', 'Montpellier', 'Munich'],
                    'duration': [{'start': 'Downtown', 'end': 'Berk', 'duration': 10},
                                 {'start': 'Berk', 'end': 'Montpellier', 'duration': 2},
                                 {'start': 'Montpellier', 'end': 'Munich', 'duration': 1}]}
        self.assertEqual(result, expected)

        result = ng1.dijkstra("Paris", 'Montpellier')
        expected = {'min': 9, 'path': ['Paris', 'Munich', 'Montpellier'],
                    'duration': [{'start': 'Paris', 'end': 'Munich', 'duration': 8},
                                 {'start': 'Munich', 'end': 'Montpellier', 'duration': 1}]}
        self.assertEqual(result, expected)

        result = ng1.dijkstra("Berlin", "San Francisco")
        expected = {'min': 15, 'path': ['Berlin', 'Toronto', 'San Francisco'],
                    'duration': [{'start': 'Berlin', 'end': 'Toronto', 'duration': 8},
                                 {'start': 'Toronto', 'end': 'San Francisco', 'duration': 7}]}
        self.assertEqual(result, expected)

    def test_networkxnopath(self):
        raw_data = [['pizza', 'chocolat', 2], ['macaron', 'vin', 14]]
        ng2 = NetworkxGraph(raw_data)
        try:
            result = ng2.dijkstra("pizza", 'macaron')
            self.assertTrue(False)
        except nx.exception.NetworkXNoPath:
            self.assertTrue(True)
