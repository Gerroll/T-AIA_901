import unittest
from pathFindingProcessing.utils import StationMapping
import json
from pathlib import Path


resource_test_path = Path(__file__).parent.joinpath("utils").joinpath("resource").joinpath("test-resource.json")


class TestStationmapping(unittest.TestCase):

    def test_mapping_file_integrity(self):
        sm: StationMapping = StationMapping()
        result = dict()
        result["station"] = sm.get_station()
        result["town"] = sm.get_town()
        result["department"] = sm.get_department()
        with open(resource_test_path) as f:
            expected = json.load(f)
        self.assertEqual(result, expected)

    def test_main_function(self):
        sm: StationMapping = StationMapping()

        result = sm.get_stations_from_unidentified('mulhouse')
        expected = ['gare de hasenrain', 'gare de mulhouse-dornach', 'gare de mulhouse-dornach',
                    'gare de mulhouse-dornach (tram/train)', 'gare de mulhouse-musees (tram/train)',
                    'gare de mulhouse-ville', 'gare de mulhouse-ville', 'gare de mulhouse-ville', 'gare de zu-rhein',
                    'hasenrain', 'mulhouse-dornach', 'mulhouse-dornach', 'mulhouse-dornach (tram/train)',
                    'mulhouse-musees (tram/train)', 'mulhouse-ville', 'mulhouse-ville', 'mulhouse-ville', 'zu-rhein']
        self.assertEqual(result, expected)

        result = sm.get_stations_from_unidentified('MuLhOuSe')
        expected = []
        self.assertEqual(result, expected)

        result = sm.get_stations_from_unidentified('mulhous')
        expected = []
        self.assertEqual(result, expected)

        result = sm.get_stations_from_unidentified('haut-rhin')
        expected = ['altkirch', 'altkirch', 'bantzenheim', 'bantzenheim', 'bartenheim', 'bitschwiller (haut-rhin)',
                    'bollwiller', 'bollwiller', 'breitenbach', 'cernay', 'colmar', 'colmar', 'colmar',
                    'colmar-mesanges', 'colmar-saint-joseph', 'dannemarie', 'fellering', 'flaxlanden',
                    'gare de altkirch', 'gare de altkirch', 'gare de bantzenheim', 'gare de bantzenheim',
                    'gare de bartenheim', 'gare de bitschwiller (haut-rhin)', 'gare de bollwiller',
                    'gare de bollwiller', 'gare de breitenbach', 'gare de cernay', 'gare de colmar', 'gare de colmar',
                    'gare de colmar', 'gare de colmar-mesanges', 'gare de colmar-saint-joseph', 'gare de dannemarie',
                    'gare de fellering', 'gare de flaxlanden', 'gare de graffenwald', 'gare de gunsbach-griesbach',
                    'gare de habsheim', 'gare de hasenrain', 'gare de herrlisheim-pres-colmar', 'gare de illfurth',
                    'gare de ingersheim-cite-scolaire', 'gare de kruth', 'gare de logelbach',
                    'gare de luttenbach-pres-munster', 'gare de lutterbach (haut-rhin)',
                    'gare de lutterbach (haut-rhin)', 'gare de lutterbach (haut-rhin)', 'gare de lutterbach-tram-train',
                    'gare de merxheim', 'gare de metzeral', 'gare de montreux-vieux', 'gare de moosch',
                    'gare de muhlbach-sur-munster', 'gare de mulhouse-dornach', 'gare de mulhouse-dornach',
                    'gare de mulhouse-dornach (tram/train)', 'gare de mulhouse-musees (tram/train)',
                    'gare de mulhouse-ville', 'gare de mulhouse-ville', 'gare de mulhouse-ville', 'gare de munster',
                    'gare de munster-badischhof', 'gare de oderen', 'gare de raedersheim', 'gare de ranspach',
                    'gare de rixheim', 'gare de rixheim', 'gare de rouffach', 'gare de saint-amarin',
                    'gare de saint-gilles', 'gare de saint-louis', 'gare de saint-louis',
                    'gare de saint-louis-la-chaussee', 'gare de saint-louis-la-chaussee', 'gare de sierentz',
                    'gare de staffelfelden', 'gare de tagolsheim', 'gare de thann', 'gare de thann-centre',
                    'gare de thann-saint-jacques', 'gare de turckheim', 'gare de vieux-thann', 'gare de vieux-thann zi',
                    'gare de walbach', 'gare de walheim', 'gare de wesserling',
                    'gare de wihr-au-val-soultzbach-les-bains', 'gare de willer-sur-thur', 'gare de zillisheim',
                    'gare de zu-rhein', 'graffenwald', 'gunsbach-griesbach', 'habsheim', 'hasenrain',
                    'herrlisheim-pres-colmar', 'illfurth', 'ingersheim-cite-scolaire', 'kruth', 'logelbach',
                    'luttenbach-pres-munster', 'lutterbach (haut-rhin)', 'lutterbach (haut-rhin)',
                    'lutterbach (haut-rhin)', 'lutterbach-tram-train', 'merxheim', 'metzeral', 'montreux-vieux',
                    'moosch', 'muhlbach-sur-munster', 'mulhouse-dornach', 'mulhouse-dornach',
                    'mulhouse-dornach (tram/train)', 'mulhouse-musees (tram/train)', 'mulhouse-ville', 'mulhouse-ville',
                    'mulhouse-ville', 'munster', 'munster-badischhof', 'oderen', 'raedersheim', 'ranspach', 'rixheim',
                    'rixheim', 'rouffach', 'saint-amarin', 'saint-gilles', 'saint-louis', 'saint-louis',
                    'saint-louis-la-chaussee', 'saint-louis-la-chaussee', 'sierentz', 'staffelfelden', 'tagolsheim',
                    'thann', 'thann-centre', 'thann-saint-jacques', 'turckheim', 'vieux-thann', 'vieux-thann zi',
                    'walbach', 'walheim', 'wesserling', 'wihr-au-val-soultzbach-les-bains', 'willer-sur-thur',
                    'zillisheim', 'zu-rhein']
        self.assertEqual(result, expected)

        result = sm.get_stations_from_unidentified('pizza')
        expected = []
        self.assertEqual(result, expected)
