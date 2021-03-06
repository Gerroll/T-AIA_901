import csv
import pandas as pd
import os
from pathFindingProcessing.utils.util import Util

# Adjust pandas console display
pd_width = 320
pd.set_option('display.width', pd_width)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)


class StationMapping:
    def __init__(self):
        data_file = os.path.join(os.path.dirname(__file__), 'resource', 'liste-des-gares.csv')
        raw_df: pd.DataFrame = pd.read_csv(data_file, sep=';')
        self.__data = self.__extract_data(raw_df)
        s = list(self.__data['STATION'].unique())
        s.sort()
        t = list(self.__data['TOWN'].unique())
        t.sort()
        d = list(self.__data['DEPARTMENT'].unique())
        d.sort()
        self.__station = s
        self.__town = t
        self.__department = d

    def __extract_data(self, data: pd.DataFrame):
        data = self.__filter_only_travellers(data)
        data = self.__remove_column(data)
        data = self.__to_lower(data)
        data = self.__remove_accents(data)
        return data

    @staticmethod
    def __filter_only_travellers(df: pd.DataFrame):
        is_travellers = df['VOYAGEURS'] == 'O'
        return df[is_travellers]

    @staticmethod
    def __remove_column(df: pd.DataFrame):
        target: pd.DataFrame = pd.DataFrame()

        target['STATION'] = df['LIBELLE']
        target['TOWN'] = df['COMMUNE']
        target['DEPARTMENT'] = df['DEPARTEMEN']
        return target

    @staticmethod
    def __to_lower(df: pd.DataFrame):
        target: pd.DataFrame = pd.DataFrame()

        target['STATION'] = df['STATION'].apply(str.lower)
        target['TOWN'] = df['TOWN'].apply(str.lower)
        target['DEPARTMENT'] = df['DEPARTMENT'].apply(str.lower)
        return target

    @staticmethod
    def __remove_accents(df: pd.DataFrame):
        target: pd.DataFrame = pd.DataFrame()

        target['STATION'] = df['STATION'].apply(Util.string_no_accents)
        target['TOWN'] = df['TOWN'].apply(Util.string_no_accents)
        target['DEPARTMENT'] = df['DEPARTMENT'].apply(Util.string_no_accents)
        return target

    def get_station(self):
        return self.__station

    def get_town(self):
        return self.__town

    def get_department(self):
        return self.__department

    def get_stations_from_town(self, town: str):
        is_town = self.__data['TOWN'] == town
        target = self.__data[is_town]
        targetList = list(target['STATION'])
        completeTargetList = targetList.copy()

        for t in targetList:
            completeTargetList.append('gare de ' + t)
        completeTargetList.sort()
        return completeTargetList

    def get_stations_from_department(self, department: str):
        is_department = self.__data['DEPARTMENT'] == department
        target = self.__data[is_department]
        targetList = list(target['STATION'])
        completeTargetList = targetList.copy()

        for t in targetList:
            completeTargetList.append('gare de ' + t)
        completeTargetList.sort()
        return completeTargetList

    def get_type(self, val: str):
        types = []

        if val in self.__station: types.append('station')
        if val in self.__town: types.append('town')
        if val in self.__department: types.append('department')
        return types

    def get_stations_from_unidentified(self, val: str):
        # remove 'gare de'
        if val.startswith('gare de '):
            val = val[8:]

        types: list = self.get_type(val)

        if len(types) == 0:
            return []
        if len(types) >= 1:
            if 'station' in types:
                return [val, 'gare de ' + val]
            if 'town' in types:
                return self.get_stations_from_town(val)
            if 'department' in types:
                return self.get_stations_from_department(val)


def main():
    sm: StationMapping = StationMapping()
    print('########## Nombre de gare dans le fichier ressource liste-des-gares.csv ##########')
    print(len(sm.get_station()))
    print('########## Liste exhaustive des gares ##########')
    print(sm.get_station())

    print('########## Nombre de ville dans le fichier ressource liste-des-gares.csv ##########')
    print(len(sm.get_town()))
    print('########## Liste exhaustive des villes ##########')
    print(sm.get_town())

    print('########## Nombre de département dans le fichier ressource liste-des-gares.csv ##########')
    print(len(sm.get_department()))
    print('########## Liste exhaustive des départements ##########')
    print(sm.get_department())

    print("########## Exemples de departs/arrivées acceptés par le module ##########")
    print("Pour mulhouse:")
    print(sm.get_stations_from_unidentified('mulhouse'))
    print("Pour MuLhOuSe:")
    print(sm.get_stations_from_unidentified('MuLhOuSe'))
    print("Pour mulhous:")
    print(sm.get_stations_from_unidentified('mulhous'))
    print("Pour haut-rhin:")
    print(sm.get_stations_from_unidentified('haut-rhin'))
    print("Pour pizza:")
    print(sm.get_stations_from_unidentified('pizza'))
