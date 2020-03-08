from ant import Ant
from threading import Lock, Condition

import random
import sys


class AntColony:
    def __init__(self, dothi, so_kien, so_vong_lap):
        self.dothi = dothi
        self.so_kien = so_kien
        self.so_vong_lap = so_vong_lap
        # tham số học tăng cường
        self.p = 0.1

        # condition var
        self.cv = Condition()

        self.reset()

    def reset(self):
        self.do_dai_tot_nhat = sys.maxsize
        self.duong_di_tot_nhat = None
        self.best_ma_tran_duong_di = None
        self.best_so_vong_lap_cuoi = 0

    def start(self):
        self.ants = self.create_ants()
        self.dem_vong_lap = 0

        while self.dem_vong_lap < self.so_vong_lap:
            self.iteration()

            self.cv.acquire()
            # hàm đợi threading
            self.cv.wait()

            lock = self.dothi.lock
            lock.acquire()
            self.global_updating_rule()
            lock.release()

            self.cv.release()

    # chạy vòng lặp bắt đầu cho kiến thăm đỉnh
    def iteration(self):
        self.trungbinh_dodai_duongdi = 0
        self.ant_counter = 0
        self.dem_vong_lap += 1
        print("vòng lặp: = %s" % (self.dem_vong_lap,))
        for ant in self.ants:
            print("Kiến %s bắt đầu" % (ant.ID))
            ant.start()

    # số lượng kiến
    def num_ants(self):
        return len(self.ants)

    # số lượng vòng lặp
    def num_iterations(self):
        return self.so_vong_lap

    # đếm số vòng lăp
    def iteration_counter(self):
        return self.dem_vong_lap

    # gọi hàm update
    def update(self, ant):
        lock = Lock()
        lock.acquire()

        self.ant_counter += 1

        self.trungbinh_dodai_duongdi += ant.do_dai_duong_di

        # book-keeping

        if ant.do_dai_duong_di < self.do_dai_tot_nhat:
            self.do_dai_tot_nhat = ant.do_dai_duong_di
            self.best_ma_tran_duong_di = ant.matran_duong_di
            self.duong_di_tot_nhat = ant.ds_duong_di
            self.best_so_vong_lap_cuoi = self.dem_vong_lap

        if self.ant_counter == len(self.ants):
            self.trungbinh_dodai_duongdi /= len(self.ants)
            print("Tốt nhất: %s, %s, %s, %s" % (
                self.duong_di_tot_nhat, self.do_dai_tot_nhat, self.dem_vong_lap, self.trungbinh_dodai_duongdi,))

            self.cv.acquire()
            self.cv.notify()
            self.cv.release()
        # outfile.close()
        lock.release()

    def done(self):
        return self.dem_vong_lap == self.so_vong_lap

    # gán cho mỗi con kiến một node ngẫu nhiên bắt đầu
    def create_ants(self):
        self.reset()
        ants = []
        for i in range(0, self.so_kien):
            ant = Ant(i, random.randint(0, self.dothi.so_dinh - 1), self)
            ants.append(ant)

        return ants

    # cập nhật lại ma trận pheromone cho sự bay hơi
    def global_updating_rule(self):
        pheromone = 0
        print("\nglobal pheromone update")
        for r in range(0, self.dothi.so_dinh):
            for s in range(0, self.dothi.so_dinh):
                if r != s:
                    # best tour
                    delt_tau = self.best_ma_tran_duong_di[r][s] / self.do_dai_tot_nhat
                    #tau rs
                    tau_rs = self.dothi.tau(r, s)
                    #                   ((1-p)*tau) * tau     +           delta(i,j)
                    pheromone = (((1 - self.p) * tau_rs) * tau_rs) + (self.p * delt_tau)
                    self.dothi.update_tau(r, s, pheromone)
