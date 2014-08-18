__author__ = 'bdavis'

from infrastructure.color import Color
from actor import Actor
from infrastructure.vector2 import Vector2

from OpenGL.GL import *

class GridActor(Actor):
    def __init__(self):
        super(GridActor, self).__init__()
        self._lineColor = Color(.76, .83, 1.0);
        self._axisColor = Color(1.0, .41, .6);
        self._interval = 1.0;
        self._minCoord = Vector2(-20.0, -20.0);
        self._maxCoord = Vector2(20.0, 20.0);
        self._points = []
        self._axes = [0.0] * 8
        self.recalculate_points();

    def recalculate_points(self):
        self._points = []

        x = self._minCoord.X
        while x < self._maxCoord.X:
            self._points.append(x)
            self._points.append(self._minCoord.Y)
            self._points.append(x)
            self._points.append(self._maxCoord.Y)
            x += self._interval

        y = self._minCoord.Y
        while y < self._maxCoord.Y:
            self._points.append(self._minCoord.X)
            self._points.append(y)
            self._points.append(self._maxCoord.X)
            self._points.append(y)
            y += self._interval

        self._axes[0] = self._minCoord.X;
        self._axes[1] = 0.0;
        self._axes[2] = self._maxCoord.X;
        self._axes[3] = 0.0;
        self._axes[4] = 0.0;
        self._axes[5] = self._minCoord.Y;
        self._axes[6] = 0.0;
        self._axes[7] = self._maxCoord.Y;

    def render(self):
        glEnableClientState(GL_VERTEX_ARRAY);
        glLineWidth(1.0);

        glColor4f(self._lineColor.R, self._lineColor.G, self._lineColor.B, 1.0);
        glVertexPointer(2, GL_FLOAT, 0, self._points);
        glDrawArrays(GL_LINES, 0, len(self._points)/2);

        # axes
        glColor4f(self._axisColor.R, self._axisColor.G, self._axisColor.B, 1.0);
        glVertexPointer(2, GL_FLOAT, 0, self._axes);
        glDrawArrays(GL_LINES, 0, 4);