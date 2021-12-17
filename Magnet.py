class Magnet:
    def __init__(self, x1: int, y1: int, x2: int, y2: int):
        self.position1 = [x1, y1]
        self.position2 = [x2, y2]
        self.isExist = False
        self.positive = -1
        self.negative = -1

    def put(self, positive: int):
        self.isExist = True
        self.positive = positive
        self.negative = 3 - positive

    def remove(self):
        self.isExist = False
        self.positive = -1
        self.negative = -1
