class Vector2(object):
    def __init__(self, x,y):
        self._x = x
        self._y = y

    @property
    def X(self):
        return self._x

    @X.setter
    def X(self, x):
        self._x = x

    @property
    def Y(self):
        return self._y

    @Y.setter
    def Y(self, y):
        self._y = y

Zero = Vector2(0.0,0.0)