from antgraph import AntGraph
from antcolony import AntColony
import sys

if __name__ == "__main__":
    # khởi tạo biến
    so_kien = 20
    so_lan_lap_toi_da = 12
    repetitions = 1

    # khoi tao bo du lieu
    cac_dinh = ["dinh1", "dinh2", "dinh3", "dinh4"]
    du_lieu = [[0, 20, 35, 42], [20, 0, 34, 30], [35, 34, 0, 12], [42, 30, 12, 0]]
    # xay dung mang
    so_dinh = len(du_lieu)
    dothi = AntGraph(so_dinh, du_lieu)
    best_path_vec = None
    best_path_cost = sys.maxsize
    for i in range(0, repetitions):
        dothi.reset_tau()
        ant_colony = AntColony(dothi, so_kien, so_lan_lap_toi_da)
        ant_colony.start()
        if ant_colony.best_path_cost < best_path_cost:
            best_path_vec = ant_colony.best_path_vec
            best_path_cost = ant_colony.best_path_cost

    print("\n------------------------------------------------------------")
    print("                     Results                                ")
    print("------------------------------------------------------------")
    print("\nBest path = %s" % (best_path_vec,))
    for node in best_path_vec:
        print(cac_dinh[node] + " ", )
    print("\nBest path cost = %s\n" % (best_path_cost,))

print("ABC")