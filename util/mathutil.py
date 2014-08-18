__author__ = 'bdavis'



def clamp(value, minValue, maxValue):
    return max(minValue, min(maxValue, value))