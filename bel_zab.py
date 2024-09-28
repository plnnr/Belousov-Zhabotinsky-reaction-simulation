# bel_zab.py

import math
import threading
import os
from random_generator import RandomGenerator

class BelZab:
    def __init__(self, dimension, alfa, beta, gamma):
        self.dimension = dimension
        self.alfa = alfa
        self.beta = beta
        self.gamma = gamma

        # Determine the number of cores (threads)
        self.nucleos = os.cpu_count()
        if self.nucleos is None or self.nucleos < 1:
            self.nucleos = 1  # Ensure at least one thread
        self.ventana = self.dimension // self.nucleos
        if self.ventana == 0:
            self.ventana = self.dimension  # If dimension is less than nucleos

        self.barrera = threading.Barrier(self.nucleos)

        # Initialize the 3D arrays a, b, c
        self.a = [[[0.0, 0.0] for _ in range(self.dimension)] for _ in range(self.dimension)]
        self.b = [[[0.0, 0.0] for _ in range(self.dimension)] for _ in range(self.dimension)]
        self.c = [[[0.0, 0.0] for _ in range(self.dimension)] for _ in range(self.dimension)]

        # Initialize the arrays with random numbers using RandomGenerator
        r = RandomGenerator()
        seed = 1

        for x in range(self.dimension):
            for y in range(self.dimension):
                seed = r.fishman_moore1(seed)
                self.a[x][y][0] = r.fishman_moore1Normalizar(seed)
                seed = r.fishman_moore1(seed)
                self.b[x][y][0] = r.fishman_moore1Normalizar(seed)
                seed = r.fishman_moore1(seed)
                self.c[x][y][0] = r.fishman_moore1Normalizar(seed)

        self.p = 0
        self.q = 1

    def nextGen(self):
        threads = []
        for i in range(self.nucleos):
            inicio = i * self.ventana
            if i == self.nucleos - 1:
                fin = self.dimension  # Ensure the last thread covers up to the end
            else:
                fin = (i + 1) * self.ventana
            t = threading.Thread(target=belZabTarea, args=(
                self.a, self.b, self.c, self.p, self.q,
                self.alfa, self.beta, self.gamma,
                self.dimension, inicio, fin, self.barrera))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        # Swap the indices for double buffering
        self.p, self.q = self.q, self.p

def belZabTarea(a, b, c, p, q, alfa, beta, gamma, dimension, inicio, fin, barrera):
    for x in range(inicio, fin):
        for y in range(dimension):
            c_a = 0.0
            c_b = 0.0
            c_c = 0.0
            for i in range(x - 1, x + 2):
                for j in range(y - 1, y + 2):
                    c_a += a[(i + dimension) % dimension][(j + dimension) % dimension][p]
                    c_b += b[(i + dimension) % dimension][(j + dimension) % dimension][p]
                    c_c += c[(i + dimension) % dimension][(j + dimension) % dimension][p]
            c_a /= 9.0
            c_b /= 9.0
            c_c /= 9.0

            a[x][y][q] = min(1.0, max(0.0, c_a + c_a * (alfa * c_b - gamma * c_c)))
            b[x][y][q] = min(1.0, max(0.0, c_b + c_b * (beta * c_c - alfa * c_a)))
            c[x][y][q] = min(1.0, max(0.0, c_c + c_c * (gamma * c_a - beta * c_b)))

    try:
        barrera.wait()
    except threading.BrokenBarrierError:
        pass

if __name__ == "__main__":
    # Example usage
    dimension = 100  # Size of the grid
    alfa = 1.2
    beta = 1.0
    gamma = 1.5

    bz = BelZab(dimension, alfa, beta, gamma)
    steps = 10  # Number of simulation steps

    for step in range(steps):
        bz.nextGen()
        print(f"Completed step {step + 1}")
        # Optional: Add code here to visualize or process the data
