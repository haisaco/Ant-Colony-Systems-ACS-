from threading import Lock


class AntGraph:
    def __init__(self, so_dinh, du_lieu, tau_mat=None):
        self.so_dinh = so_dinh
        self.du_lieu = du_lieu
        self.lock = Lock()
        # tau mat contains the amount of phermone at node x,y
        if tau_mat is None:
            self.tau_mat = []
            for i in range(0, so_dinh):
                self.tau_mat.append([0] * so_dinh)

    def delta(self, r, s):
        return self.du_lieu[r][s]

    def tau(self, r, s):
        return self.tau_mat[r][s]

        # 1 / delta = etha

    def etha(self, r, s):
        return 1.0 / self.delta(r, s)

    # cap nhat lai gia tri pheromone
    def update_tau(self, r, s, val):
        lock = Lock()
        lock.acquire()
        self.tau_mat[r][s] = val
        lock.release()

    # reset lại pheromone
    def reset_tau(self):
        lock = Lock()
        lock.acquire()
        avg = self.average_delta()

        # khởi tao tau ban đầu
        self.tau0 = 1.0 / (self.so_dinh * 0.5 * avg)

        print("Average = %s" % (avg,))
        print("Tau0 = %s" % (self.tau0))

        for r in range(0, self.so_dinh):
            for s in range(0, self.so_dinh):
                self.tau_mat[r][s] = self.tau0
        lock.release()

    # giá trị trung bình của delta
    def average_delta(self):
        return self.average(self.du_lieu)

    # giá trị trung bình của tau
    def average_tau(self):
        return self.average(self.tau_mat)

    # tính giá trị trung bình ma trận khoảng cách
    def average(self, matrix):
        sum = 0
        for r in range(0, self.so_dinh):
            for s in range(0, self.so_dinh):
                sum += matrix[r][s]

        avg = sum / (self.so_dinh * self.so_dinh)
        return avg
