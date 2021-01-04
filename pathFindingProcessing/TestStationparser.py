import unittest
from pathFindingProcessing.utils import StationParser
import json
from pathlib import Path


original_csv_station = Path(__file__).parent.joinpath("utils").joinpath("resource").joinpath("original-csv-station.json")


class TestStationparser(unittest.TestCase):

    def test_original_csv_integrity(self):
        sp = StationParser()
        result = dict()
        result["station"] = sp.get_stations()
        with open(original_csv_station) as f:
            expected = json.load(f)
        self.assertEqual(result, expected)
