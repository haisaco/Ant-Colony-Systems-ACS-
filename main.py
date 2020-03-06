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
    duong_di_tot_nhat = None
    do_dai_tot_nhat = sys.maxsize
    for i in range(0, repetitions):
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
    for node in duong_di_tot_nhat:
        print(cac_dinh[node] + " ", )
    print("\nĐộ dài tốt nhất = %s\n" % (do_dai_tot_nhat,))
