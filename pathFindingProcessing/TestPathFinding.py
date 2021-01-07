import unittest
from pathFindingProcessing.pathfinder import PathFinder


class TestPathFinding(unittest.TestCase):

    def test_find_path_networkx(self):
        pf = PathFinder()

        result = pf.find_path_networkx("gare de paris-est", "vosges")
        expected = {'min': 227,
                    'path': ['gare de paris-est', 'gare de chaumont', 'gare de culmont-chalindrey', 'gare de vittel'],
                    'duration': [{'start': 'gare de paris-est', 'end': 'gare de chaumont', 'duration': 145},
                                 {'start': 'gare de chaumont', 'end': 'gare de culmont-chalindrey', 'duration': 33},
                                 {'start': 'gare de culmont-chalindrey', 'end': 'gare de vittel', 'duration': 49}]}
        self.assertEqual(result, expected)

        result = pf.find_path_networkx("gare de quimper", "gare de laval")
        expected = {'min': 196, 'path': ['gare de quimper', 'gare de rennes', 'gare de laval'],
                    'duration': [{'start': 'gare de quimper', 'end': 'gare de rennes', 'duration': 141},
                                 {'start': 'gare de rennes', 'end': 'gare de laval', 'duration': 55}]}
        self.assertEqual(result, expected)

        result = pf.find_path_networkx("gare de le mans", "paris")
        expected = {'min': 209, 'path': ['gare de le mans', 'gare de chartres', 'gare de voves', 'gare de chateaudun',
                                         'gare de paris-austerlitz'],
                    'duration': [{'start': 'gare de le mans', 'end': 'gare de chartres', 'duration': 70},
                                 {'start': 'gare de chartres', 'end': 'gare de voves', 'duration': 23},
                                 {'start': 'gare de voves', 'end': 'gare de chateaudun', 'duration': 21},
                                 {'start': 'gare de chateaudun', 'end': 'gare de paris-austerlitz', 'duration': 95}]}
        self.assertEqual(result, expected)
