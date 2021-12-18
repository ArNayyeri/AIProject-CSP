class Magnet:
    def __init__(self, x1: int, y1: int, x2: int, y2: int):
        self.position = []
        self.position.append([x1, y1])
        self.position.append([x2, y2])
        self.isExist = False
        self.positive = -1
        self.negative = -1

    def put(self, positive_pos: int):
        self.isExist = True
        self.positive = positive_pos
        self.negative = 1 - positive_pos

    def remove(self):
        self.isExist = False
        self.positive = -1
        self.negative = -1

    def get_positive_pos(self):
        if not self.isExist:
            return -1
        return self.position[self.positive]

    def get_negative_pos(self):
        if not self.isExist:
            return -1
        return self.position[self.negative]
