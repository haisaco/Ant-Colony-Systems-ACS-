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

        #
        self.Beta = 1
        # khởi tạo giá trị q ban đầu
        self.Q0 = 0.5
        # chỉ số p
        self.Rho = 0.1

        # các đỉnh còn lại chưa đc thăm
        self.dinh_ghe_tham = {}

        for i in range(0, self.dothi.so_dinh):
            if i != self.dinh_bat_dau:
                self.dinh_ghe_tham[i] = i

        # khởi tạo ma trận đường đi =0
        self.matran_duong_di = []

        for i in range(0, self.dothi.so_dinh):
            self.matran_duong_di.append([0] * self.dothi.so_dinh)

    # hàm Thread run()
    def run(self):
        dothi = self.thongtin.dothi
        while not self.end():

            dothi.lock.acquire()
            new_node = self.state_transition_rule(self.dinh_hien_tai)
            self.do_dai_duong_di += dothi.delta(self.dinh_hien_tai, new_node)

            self.ds_duong_di.append(new_node)
            self.matran_duong_di[self.dinh_hien_tai][new_node] = 1  # đường đi của kiến dưới dạng ma trận

            print("Ant %s : %s, %s" % (self.ID, self.ds_duong_di, self.do_dai_duong_di,))

            self.local_updating_rule(self.dinh_hien_tai, new_node)
            dothi.lock.release()

            self.dinh_hien_tai = new_node

        # cập nhật độ dài đường đi qua mỗi lần kiến thăm đỉnh
        # self.do_dai_duong_di += dothi.delta(self.ds_duong_di[-1], self.ds_duong_di[0])

        # gửi kết quả ra ngoài colony
        self.thongtin.update(self)
        print("Tiến trình kiến %s chấm dứt." % (self.ID,))
        print("===============================================\n")

        # khởi tạo lại luồng
        self.__init__(self.ID, self.dinh_bat_dau, self.thongtin)

    def end(self):
        return not self.dinh_ghe_tham

    # điều kiện chọn đỉnh thăm tiếp theo
    def state_transition_rule(self, dinh_hien_tai):
        dothi = self.thongtin.dothi
        q = random.random()
        max_node = -1

        if q < self.Q0:
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
            sum = 0
            node = -1

            for node in self.dinh_ghe_tham.values():
                if dothi.tau(dinh_hien_tai, node) == 0:
                    raise Exception("tau = 0")
                sum += dothi.tau(dinh_hien_tai, node) * math.pow(dothi.etha(dinh_hien_tai, node), self.Beta)
            if sum == 0:
                raise Exception("sum = 0")

            avg = sum / len(self.dinh_ghe_tham)

            # print("trung bình = %s" % (avg,))

            for node in self.dinh_ghe_tham.values():
                p = dothi.tau(dinh_hien_tai, node) * math.pow(dothi.etha(dinh_hien_tai, node), self.Beta)
                if p > avg:
                    # print("p = %s" % (p,))
                    max_node = node

            if max_node == -1:
                max_node = node

        if max_node < 0:
            raise Exception("max_node < 0")

        del self.dinh_ghe_tham[max_node]
        print("Đỉnh thăm tiếp theo %s :\n" % (max_node))
        return max_node

    # cập nhật lại local pheromone
    def local_updating_rule(self, dinh_hien_tai, next_node):
        print("update pheromone local tại đỉnh %s." % (dinh_hien_tai))
        dothi = self.thongtin.dothi
        val = (1 - self.Rho) * dothi.tau(dinh_hien_tai, next_node) + (self.Rho * dothi.tau0)
        dothi.update_tau(dinh_hien_tai, next_node, val)
