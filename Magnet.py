
class Magnet:
    def __init__(self, x1: int, y1: int,
                 x2: int, y2: int):
        self.position = []

        self.position.append([x1, y1])
        self.position.append([x2, y2])

        self.isExist = False
        self.isEmpty = False

        self.init_domain = [[x1, y1 , True] , [x1, y1 , False] , 0]
        self.domain = self.init_domain

        self.positive = -1
        self.negative = -1

    def put(self, x: int, y: int, positive: bool):
        self.isExist = True

        if positive:
            if self.position[0] == [x, y]:
                self.positive = 0
            elif self.position[1] == [x, y]:
                self.positive = 1

            self.negative = 1 - self.positive

        else:
            if self.position[0] == [x, y]:
                self.negative = 0
            elif self.position[1] == [x, y]:
                self.negative = 1

            self.positive = 1 - self.negative

    def get_domain(self):
        return self.domain

    def remove(self):
        self.isExist = False
        self.positive = -1
        self.negative = -1

    def get_position(self):
        return self.position[0]

    def get_positive_pos(self):
        if not self.isExist:
            return [-1,-1]
        return self.position[self.positive]

    def get_negative_pos(self):
        if not self.isExist:
            return [-1,-1]
        return self.position[self.negative]
