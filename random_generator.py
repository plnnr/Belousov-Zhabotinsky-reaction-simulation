# random_generator.py

import math

class RandomGenerator:

    def __init__(self):
        # Initialize constants
        self.a = int(math.pow(7, 5))
        self.dosE31menos1 = int(math.pow(2, 31) - 1)
        self.q = self.dosE31menos1 // self.a
        self.r = self.dosE31menos1 % self.a
        self.dosE31menos1Double = 2147483647.0

    def random(self, semilla, nNum):
        if nNum == 0:
            return 0
        return self.random(((5 * semilla) + 1) % 16, nNum - 1)

    def ejemplo26_1a(self, semilla):
        return (5 * semilla) % int(math.pow(2, 5))

    def ejemplo26_1b(self, semilla):
        return (7 * semilla) % int(math.pow(2, 5))

    def ejemplo26_2(self, semilla):
        return (3 * semilla) % 31

    def ejemplo26_3(self, semilla, nNum):
        for _ in range(nNum):
            x_div_q = semilla // self.q
            x_mod_q = semilla % self.q
            semilla_new = (self.a * x_mod_q) - (self.r * x_div_q)
            if semilla_new > 0:
                semilla = semilla_new
            else:
                semilla = semilla_new + self.dosE31menos1
        return semilla

    def UnEjemplo26_3(self, semilla):
        x_div_q = semilla // self.q
        x_mod_q = semilla % self.q
        semilla_new = (self.a * x_mod_q) - (self.r * x_div_q)
        if semilla_new > 0:
            semilla = semilla_new
        else:
            semilla = semilla_new + self.dosE31menos1
        return semilla

    def UnEjemplo26_42(self, s):
        cien57 = 157
        cien46 = 146
        cien42 = 142
        qW = 32363
        qX = 31727
        qY = 31657
        qWmenos1 = 32362

        s[0] = (cien57 * s[0]) % qW
        s[1] = (cien46 * s[1]) % qX
        s[2] = (cien42 * s[2]) % qY
        s[3] = (s[0] - s[1] + s[2]) % qWmenos1

        return s[3]

    def fishman_moore1(self, semilla):
        m = 48271
        return (m * semilla) % self.dosE31menos1

    def fishman_moore1Normalizar(self, seed):
        return seed / self.dosE31menos1Double

    def fishman_moore2(self, semilla):
        m = 69621
        return (m * semilla) % self.dosE31menos1

    def randu(self, semilla):
        dosE16mas3 = int(math.pow(2, 16) + 3)
        return (dosE16mas3 * semilla) % (self.dosE31menos1 + 1)

if __name__ == "__main__":
    seed = 1
    r = RandomGenerator()
    for _ in range(640):
        seed = r.fishman_moore1(seed)
        print(r.fishman_moore1Normalizar(seed))
