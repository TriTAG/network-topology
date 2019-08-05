import math
from collections import namedtuple

_point = namedtuple('Point', ('x', 'y'))


class Point(_point):

    def __new__(cls, *args, **kwargs):
        if not kwargs and len(args) == 2:
            return super().__new__(cls, x=float(args[0]), y=float(args[1]))
        elif not args and set(kwargs) == {'x', 'y'}:
            return super().__new__(cls, x=float(kwargs['x']), y=float(kwargs['y']))
        else:
            raise TypeError('Invalid arguments')

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __add__(self, other):
        if isinstance(other, Point):
            return Point(self.x+other.x, self.y+other.y)
        elif isinstance(other, tuple):
            return Point(self.x+other[0], self.y+other[1])
        else:
            raise TypeError('Expected Point or tuple.')

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, Point):
            return Point(self.x-other.x, self.y-other.y)
        elif isinstance(other, tuple):
            return Point(self.x-other[0], self.y-other[1])
        else:
            raise TypeError('Expected Point or tuple.')

    def __rsub__(self, other):
        return -self.__sub__(other)

    def __mul__(self, factor):
        if isinstance(factor, (float, int)):
            return Point(self.x*factor, self.y*factor)
        else:
            raise TypeError('Expected float or int.')

    def __rmul__(self, factor):
        return self.__mul__(factor)

    def __truediv__(self, divisor):
        if isinstance(divisor, (float, int)):
            return Point(self.x/divisor, self.y/divisor)
        else:
            raise TypeError('Expected float or int.')

    def __abs__(self):
        return math.sqrt(self.x**2 + self.y**2)
