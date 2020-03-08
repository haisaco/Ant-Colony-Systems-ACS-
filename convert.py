import re


class Convert:
    def __init__(self, tsp_name):
        self.tsp_name = tsp_name
        self.dinh = []
        self.cities = []
        self.points = []
        self.get_datas()

    def get_datas(self):
        with open(self.tsp_name) as f:
            for line in f.readlines():
                city = line.split(' ')
                self.cities.append(dict(index=int(city[0]), x=int(city[1]), y=int(city[2])))
                self.points.append((int(city[1]), int(city[2])))
                self.dinh.append(city[0])
