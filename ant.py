import math
import random
import sys
from threading import *


class Ant(Thread):
    def __init__(self, ID, dinh_bat_dau, thongtin):
        Thread.__init__(self)
        self.ID = ID
        self.dinh_bat_dau = dinh_bat_dau
        self.thongtin = thongtin

        self.dinh_hien_tai = self.dinh_bat_dau
        self.dothi = self.thongtin.dothi
        self.ds_duong_di = []
        self.ds_duong_di.append(self.dinh_bat_dau)
        self.do_dai_duong_di = 0

        # same meaning as in standard equations
        self.Beta = 1
        # self.Q0 = 1  # Q0 = 1 works just fine for 10 city case (no explore)
        self.Q0 = 0.5
        self.Rho = 0.99

        # store the nodes remaining to be explored here
        self.dinh_ghe_tham = {}

        for i in range(0, self.dothi.so_dinh):
            if i != self.dinh_bat_dau:
                self.dinh_ghe_tham[i] = i

        # create n X n matrix 0'd out to start
        self.path_mat = []

        for i in range(0, self.dothi.so_dinh):
            self.path_mat.append([0] * self.dothi.so_dinh)

    # overide Thread's run()
    def run(self):
        dothi = self.thongtin.dothi
        while not self.end():
            # we need exclusive access to the graph
            dothi.lock.acquire()
            new_node = self.state_transition_rule(self.dinh_hien_tai)
            self.do_dai_duong_di += dothi.delta(self.dinh_hien_tai, new_node)

            self.ds_duong_di.append(new_node)
            self.path_mat[self.dinh_hien_tai][new_node] = 1  # adjacency matrix representing path

            print("Ant %s : %s, %s" % (self.ID, self.ds_duong_di, self.do_dai_duong_di,))
            print("Path_math %s" % (self.path_mat))

            self.local_updating_rule(self.dinh_hien_tai, new_node)
            dothi.lock.release()

            self.dinh_hien_tai = new_node

        # don't forget to close the tour
        self.do_dai_duong_di += dothi.delta(self.ds_duong_di[-1], self.ds_duong_di[0])

        # send our results to the colony
        self.thongtin.update(self)
        print("Ant thread %s terminating." % (self.ID,))

        # allows thread to be restarted (calls Thread.__init__)
        self.__init__(self.ID, self.dinh_bat_dau, self.thongtin)

    def end(self):
        return not self.dinh_ghe_tham

        # described in report -- determines next node to visit after curr_node

    def state_transition_rule(self, dinh_hien_tai):
        dothi = self.thongtin.dothi
        q = random.random()
        max_node = -1

        if q < self.Q0:
            print("Exploitation")
            max_val = -1
            val = None

            for node in self.dinh_ghe_tham.values():
                if dothi.tau(dinh_hien_tai, node) == 0:
                    raise Exception("tau = 0")

                val = dothi.tau(dinh_hien_tai, node) * math.pow(dothi.etha(dinh_hien_tai, node), self.Beta)
                if val > max_val:
                    max_val = val
                    max_node = node
        else:
            print("Exploration")
            sum = 0
            node = -1

            for node in self.dinh_ghe_tham.values():
                if dothi.tau(dinh_hien_tai, node) == 0:
                    raise Exception("tau = 0")
                sum += dothi.tau(dinh_hien_tai, node) * math.pow(dothi.etha(dinh_hien_tai, node), self.Beta)
            if sum == 0:
                raise Exception("sum = 0")

            avg = sum / len(self.dinh_ghe_tham)

            print("avg = %s" % (avg,))

            for node in self.dinh_ghe_tham.values():
                p = dothi.tau(dinh_hien_tai, node) * math.pow(dothi.etha(dinh_hien_tai, node), self.Beta)
                if p > avg:
                    print("p = %s" % (p,))
                    max_node = node

            if max_node == -1:
                max_node = node

        if max_node < 0:
            raise Exception("max_node < 0")

        del self.dinh_ghe_tham[max_node]

        return max_node

    # phermone update rule for indiv ants
    def local_updating_rule(self, dinh_hien_tai, next_node):
        dothi = self.thongtin.dothi
        val = (1 - self.Rho) * dothi.tau(dinh_hien_tai, next_node) + (self.Rho * dothi.tau0)
        dothi.update_tau(dinh_hien_tai, next_node, val)
