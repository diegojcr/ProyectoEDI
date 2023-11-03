class PrivateKey:
    def __init__(self, n, j, z):
        self.n = n
        self.j = j
        self.z = z

    def getN(self):
        return self.n

    def getJ(self):
        return self.j