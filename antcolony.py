from ant import Ant
from threading import Lock, Condition

import random
import sys


class AntColony:
    def __init__(self, dothi, num_ants, num_iterations):
        self.dothi = dothi
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.Alpha = 0.1

        # condition var
        self.cv = Condition()

        self.reset()

    def reset(self):
        self.do_dai_tot_nhat = sys.maxsize
        self.duong_di_tot_nhat = None
        self.best_ma_tran_duong_di = None
        self.last_best_path_iteration = 0

    def start(self):
        self.ants = self.create_ants()
        self.iter_counter = 0

        while self.iter_counter < self.num_iterations:
            self.iteration()

            self.cv.acquire()
            # wait until update calls notify()
            self.cv.wait()

            lock = self.dothi.lock
            lock.acquire()
            self.global_updating_rule()
            lock.release()

            self.cv.release()

    # one iteration involves spawning a number of ant threads
    def iteration(self):
        self.avg_path_cost = 0
        self.ant_counter = 0
        self.iter_counter += 1
        print("iter_counter = %s" % (self.iter_counter,))
        for ant in self.ants:
            print("starting ant = %s" % (ant.ID))
            ant.start()

    def num_ants(self):
        return len(self.ants)

    def num_iterations(self):
        return self.num_iterations

    def iteration_counter(self):
        return self.iter_counter

    # called by individual ants
    def update(self, ant):
        lock = Lock()
        lock.acquire()

        # outfile = open("results.dat", "a")

        print("Update called by %s" % (ant.ID,))
        self.ant_counter += 1

        self.avg_path_cost += ant.do_dai_duong_di

        # book-keeping

        if ant.do_dai_duong_di < self.do_dai_tot_nhat:
            self.do_dai_tot_nhat = ant.do_dai_duong_di
            self.best_ma_tran_duong_di = ant.path_mat
            self.duong_di_tot_nhat = ant.ds_duong_di
            self.last_best_path_iteration = self.iter_counter

        if self.ant_counter == len(self.ants):
            self.avg_path_cost /= len(self.ants)
            print("Math_s %s" % (self.best_ma_tran_duong_di))
            print("Best: %s, %s, %s, %s" % (
            self.duong_di_tot_nhat, self.do_dai_tot_nhat, self.iter_counter, self.avg_path_cost,))
            # outfile.write("\n%s\t%s\t%s" % (self.iter_counter, self.avg_path_cost, self.do_dai_tot_nhat,))
            self.cv.acquire()
            self.cv.notify()
            self.cv.release()
        # outfile.close()
        lock.release()

    def done(self):
        return self.iter_counter == self.num_iterations

    # assign each ant a random start-node
    def create_ants(self):
        self.reset()
        ants = []
        for i in range(0, self.num_ants):
            ant = Ant(i, random.randint(0, self.dothi.so_dinh - 1), self)
            ants.append(ant)

        return ants

    # changes the tau matrix based on evaporation/deposition
    def global_updating_rule(self):
        evaporation = 0
        deposition = 0

        for r in range(0, self.dothi.so_dinh):
            for s in range(0, self.dothi.so_dinh):
                if r != s:
                    delt_tau = self.best_ma_tran_duong_di[r][s] / self.do_dai_tot_nhat
                    evaporation = (1 - self.Alpha) * self.dothi.tau(r, s)
                    deposition = self.Alpha * delt_tau

                    self.dothi.update_tau(r, s, evaporation + deposition)
