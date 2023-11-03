class PublicKey:
    def __init__(self, n, k, z):
        self.n = n
        self.k = k
        self.z = z

    def getN(self):
        return self.n

    def getK(self):
        return self.k

    def getZ(self):
        return self.z
