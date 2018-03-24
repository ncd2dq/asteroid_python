class Vector(object):
    def __init__(self, vec):
        self.x = vec[0]
        self.y = vec[1]

    def __add__(self, other):
        new_x, new_y = self.x + other.x, self.y + other.y
        return Vector((new_x, new_y))

    def _mult(self, scalar):
        new_x, new_y = self.x * scalar, self.y * scalar

    def _normalize(self):
        mag = self.magnitude()
        new_x, new_y = self.x / mag, self.y / mag

    def _magnitude(self):
        mag = (self.x * self.x + self.y * self.y)^(0.5)
        return mag

    def __sub__(self, other):
        new_x, new_y = self.x - other.x, self.y - other.y