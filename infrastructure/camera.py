__author__ = 'bdavis'

from OpenGL.GL import *
from OpenGL.GLU import *

from vector3 import Vector3
from actors.actor import Actor

class Camera(Actor):
    def __init__(self):
        super(Camera,self).__init__()

        self.aperture = 90.0
        self.camera3dPosition = Vector3(0.0,0.0,10.0)
        self.view = Vector3(0.0, 0.0, -10.0);
        self.up = Vector3(0.0, 1.0, 0.0);
        self.zNearClip = 0.001;
        self.zFarClip = 200.0;
        #self.locked = NULL;

    def render(self):
        glMatrixMode(GL_MODELVIEW);
        glLoadIdentity();
        glRotatef(super(Camera,self).rotation, 0.0, 0.0, 1.0);
        gluLookAt(self.camera3dPosition.X, self.camera3dPosition.Y, self.camera3dPosition.Z,
            self.camera3dPosition.X + self.view.X,
            self.camera3dPosition.Y + self.view.Y,
            self.camera3dPosition.Z + self.view.Z,
            self.up.X, self.up.Y, self.up.Z
        )

    @property
    def position(self):
        return self.camera3dPosition

    @position.setter
    def position(self, position):
        self.camera3dPosition = position

    def update(self, dt):
        super(Camera, self).update(dt)

    def resize(self, width, height):
        print("resize")

        self._windowHeight = height;
        self._windowWidth = width;

        glViewport(0, 0, self._windowWidth, self._windowHeight);

        glMatrixMode(GL_PROJECTION);
        glLoadIdentity();
        aspect = float(self._windowWidth)/float(self._windowHeight)
        gluPerspective(self.aperture, aspect, self.zNearClip, self.zFarClip);
        glMatrixMode(GL_MODELVIEW);




camera = Camera()

def resize(width, height):
    camera.resize(width, height)