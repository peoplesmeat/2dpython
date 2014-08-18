__author__ = 'bdavis'


class Color:
    def __init__(self,r = 1.0,g = 1.0,b = 1.0,a = 1.0):
        self.R = r
        self.G = g
        self.B = b
        self.A = a


    def from_ints(r,g,b,a):
        return Color(r/255.0, g/255.0, b/255.0, a/255.0)
