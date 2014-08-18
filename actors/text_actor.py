__author__ = 'bdavis'

from infrastructure.vector2 import Zero
from infrastructure.text_rendering import *


class TextNugget(object):
    def __init__(self, text):
        self.text = text

class TextActor(Actor):
    def __init__(self, fontNickname, displayString, align, lineSpacing):
        self._color = Color(0.0,0.0,0.0)
        self._fontNamename = fontNickname
        self._alignment = align
        self._lineSpacing = lineSpacing
        self._screenPosition = vector2.Zero

        set_display_string(displayString)

    def set_display_string(self, displayString):
        self.rawString = displayString
        self.displayStrings = []
        for s in displayString.split("\n"):
            self.displayString.append(TextNugget(s))

        self.calculate_position()

    def get_text_extents(self, text, fontNickname):


    def calculate_position(self):
        largest = Zero
        for i in self.displayStrings:
            i.extents = get_text_extents(i.text, self._fontNamename)
            largest.X = i.extents.X if i.extents.X > largest.X else largest.X
            largest.Y = i.extents.Y if i.extents.Y > largest.Y else largest.Y


