

class Vector3(object):
    def __init__(self, x,y,z):
        self._x = x
        self._y = y
        self._z = z


    X = property(lambda self: self._x)
    Y = property(lambda self: self._y)
    Z = property(lambda self: self._z)