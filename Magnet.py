class Magnet:
    def __init__(self, x1: int, y1: int,
                 x2: int, y2: int):
        self.position = []

        self.history = {}

        self.position.append([x1, y1])
        self.position.append([x2, y2])

        self.isExist = False
        self.isEmpty = False

        self.init_domain = [[x1, y1, False], [x1, y1, True], 0]
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

    def check_domain(self, domain):
        mydomain = self.get_domain()

        r_domains = []

        for _mydomain in mydomain:

            if _mydomain == 0:
                continue

            removeddomain = None

            if domain[0] + 1 == _mydomain[0] and domain[1] == _mydomain[1] and domain[2] == _mydomain[2]:
                removeddomain = _mydomain
            if domain[0] - 1 == _mydomain[0] and domain[1] == _mydomain[1] and domain[2] == _mydomain[2]:
                removeddomain = _mydomain

            if domain[0] == _mydomain[0] and domain[1] + 1 == _mydomain[1] and domain[2] == _mydomain[2]:
                removeddomain = _mydomain
            if domain[0] == _mydomain[0] and domain[1] - 1 == _mydomain[1] and domain[2] == _mydomain[2]:
                removeddomain = _mydomain

            # if domain[0] + 1 == self.position[1][0] and domain[1] == self.position[1][1] and domain[2] != _mydomain[2]:
            #     removeddomain = _mydomain
            # if domain[0] - 1 == self.position[1][0] and domain[1] == self.position[1][1] and domain[2] != _mydomain[2]:
            #     removeddomain = _mydomain

            # if domain[0] == self.position[1][0] and domain[1] + 1 == self.position[1][1] and domain[2] != _mydomain[2]:
            #     removeddomain = _mydomain
            # if domain[0] == self.position[1][0] and domain[1] - 1 == self.position[1][1] and domain[2] != _mydomain[2]:
            #     removeddomain = _mydomain

            if removeddomain is not None:
                r_domains.append(removeddomain)
                self.domain.remove(removeddomain)

        return r_domains

    def add_to_domain(self, domain):
        self.domain.insert(0, domain)

    def get_domain(self):
        return self.domain

    def remove(self):
        self.isExist = False
        self.isEmpty = False
        self.positive = -1
        self.negative = -1

    def get_position(self):
        return self.position[0]

    def get_positive_pos(self):
        if not self.isExist:
            return [-1, -1]
        return self.position[self.positive]

    def get_negative_pos(self):
        if not self.isExist:
            return [-1, -1]
        return self.position[self.negative]
