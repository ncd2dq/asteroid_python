class Vector(object):
    def __init__(self, vec):
        self.x = vec[0]
        self.y = vec[1]

    def __add__(self, other):
        new_x, new_y = self.x + other.x, self.y + other.y
        return Vector((new_x, new_y))

    def _mult(self, scalar):
        new_x, new_y = self.x * scalar, self.y * scalar
        return Vector((new_x, new_y))

    def _normalize(self):
        mag = self._magnitude()
        new_x, new_y = self.x / mag, self.y / mag
        self.x, self.y = new_x, new_y

    def _direction(self):
        mag = self._magnitude()
        new_x, new_y = self.x / mag, self.y / mag
        unit_direction = Vector((new_x, new_y))
        return unit_direction

    def classify_direction(self, direction='up'):
        ''' direction='x' or direction='y' will return 'left','right','up','down' '''

        if direction == 'x':
            if self.x > 0:
                return 'right'
            if self.x < 0:
                return 'left'
            if self.x == 0:
                return None

        if direction =='y':
            if self.y > 0:
                return 'down'
            if self.y < 0:
                return 'up'
            if self.y == 0:
                return None

    def _magnitude(self):
        mag = (self.x * self.x + self.y * self.y)**(0.5)
        return mag

    def __sub__(self, other):
        new_x, new_y = self.x - other.x, self.y - other.y
        return Vector((new_x, new_y))

    def __str__(self):
        return '<' + str(self.x) +',' + ' ' + str(self.y) + '>'