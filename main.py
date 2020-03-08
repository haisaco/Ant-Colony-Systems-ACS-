from convert import Convert

from antgraph import AntGraph
from antcolony import AntColony
import sys
import math


def distance(city1: dict, city2: dict):
    return math.sqrt((city1['x'] - city2['x']) ** 2 + (city1['y'] - city2['y']) ** 2)


if __name__ == "__main__":
    src = Convert("./data/eil51.tsp")
    # khởi tạo biến
    so_kien = 10
    so_lan_lap_toi_da = 5
    so_lan_chay = 1

    # khoi tao bo du lieu
    cac_dinh = src.dinh
    # ["dinh1", "dinh2", "dinh3", "dinh4"]
    # [[0, 20, 35, 42], [20, 0, 34, 30], [35, 34, 0, 12], [42, 30, 12, 0]]

    cost_matrix = []
    rank = len(src.cities)
    for i in range(rank):
        row = []
        for j in range(rank):
            row.append(distance(src.cities[i], src.cities[j]))
        cost_matrix.append(row)

    du_lieu = cost_matrix

    # xay dung mang
    so_dinh = len(du_lieu)
    dothi = AntGraph(so_dinh, du_lieu)
    duong_di_tot_nhat = None
    do_dai_tot_nhat = sys.maxsize
    for i in range(0, so_lan_chay):
        dothi.reset_tau()
        ant_colony = AntColony(dothi, so_kien, so_lan_lap_toi_da)
        ant_colony.start()
        if ant_colony.do_dai_tot_nhat < do_dai_tot_nhat:
            duong_di_tot_nhat = ant_colony.duong_di_tot_nhat
            do_dai_tot_nhat = ant_colony.do_dai_tot_nhat

    print("\n------------------------------------------------------------")
    print("                     Kết quả                                ")
    print("------------------------------------------------------------")
    print("\nĐường đi tốt nhất = %s" % (duong_di_tot_nhat,))
    #for node in duong_di_tot_nhat:
    #   print(cac_dinh[node] + " ", )
    print("\nĐộ dài tốt nhất = %s\n" % (do_dai_tot_nhat,))
