from __future__ import absolute_import

__author__ = 'bdavis'

from OpenGL.GL import *
from OpenGL.GLU import *

import glfw
from . import camera
import time
import logging
from actors.grid_actor import GridActor


from util import mathutil

logger = logging.getLogger()

class FpsCounter(object):
    def __init__(self, interval = 1.0):
        self.interval = interval
        self.frames = 0
        self.currTime = time.time()
        self.prevTime = self.currTime

    def increment_frame(self):
        self.frames+=1
        self.currTime = time.time()
        if (self.currTime - self.prevTime) > self.interval:
            fps = (1.0/((self.currTime - self.prevTime)/self.frames))
            logger.info("%s fps: %s, frames: %s" % (self.currTime, fps, self.frames))
            #logger.info(str(self.currTime) + " fps: " + str(fps) + " " + str(self.currTime - self.prevTime))
            self.prevTime = self.currTime
            self.frames = 0


class World(object):
    def __init__(self):
        self.initialized = False

        self.fps = FpsCounter(5.0)

        self.currTime = time.time()

        self.actors = {0 : [GridActor()]}
        self.prevTime = time.time()

        self.deferred_layer_changes = []

    def add(self, actor, layer = 0 ):
        if self.actors.has_key(layer):
            self.actors[layer].append(actor)
        else:
            self.actors[layer] = [actor]


    def initialize(self, windowWidth, windowHeight, windowName, antiAliasing, fullScreen, resizable):
        if self.initialized:
            return False

        self.running = True

        glfw.Init()


        if antiAliasing:
            glfw._glfwdll.glfwOpenWindowHint(glfw.FSAA_SAMPLES, 4)

        windowMode = glfw.WINDOW
        if fullScreen:
            windowMode = glfw.FULLSCREEN

        if resizable:
            #glfw.OpenWindowHint(glfw.WINDOW_NO_RESIZE, 0);
            pass

        print(glfw.GetGLVersion())

        glfw.OpenWindow(windowWidth, windowHeight, 0, 0, 0, 8, 0, 0, windowMode)
        glfw.SetWindowTitle(windowName)
        glfw.SetWindowPos(50,50)

        glfw.SwapInterval(1)
        glfw.SetWindowSizeCallback(camera.resize)

        glfw.Disable(glfw.KEY_REPEAT)

        #prevTime = glfw.GetT

        glClearDepth(1.0);
        glPolygonMode(GL_FRONT, GL_FILL)

        glShadeModel(GL_FLAT)

        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
        glEnable(GL_CULL_FACE)
        glFrontFace(GL_CCW)
        glCullFace(GL_BACK)
        glDepthFunc(GL_LEQUAL)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glClearStencil(0)
        glClearColor(1.0, 1.0, 1.0, 1.0)


    def calculate_dt(self):
        self.currTime = time.time()
        dt = self.currTime - self.prevTime
        self.prevTime = self.currTime
        return mathutil.clamp(dt, 0, 1.0)

    def tick(self):
        frame_dt = self.calculate_dt()

        camera.camera.update(frame_dt)

        for layer, actor_list in self.actors.iteritems() :
            for actor in actor_list:
                actor.update(frame_dt)

        self.process_deferred_layer_changes()

    def process_deferred_layer_changes(self):
        for layer_change in self.deferred_layer_changes:
            self.remove(layer_change[0])
            self.add(layer_change[0], layer_change[1])
        self.deferred_layer_changes = []

    def remove(self, actor):
        for l in self.actors.itervalues():
            try:
                l.remove(actor)
                logger.debug("Removed id:%s" % (actor.id))
            except:
                logger.warn("failed to remove actor %s" %( actor.id ) )

    def render(self):
        camera.camera.render()

        for layer, actor_list in self.actors.iteritems() :
            for actor in actor_list:
                actor.render()

        self.fps.increment_frame()


    def tick_and_render(self):
        self.tick()
        self.render()

    def start(self):
        self.running = True
        GL_DEPTH_BUFFER_BIT      =         0x00000100
        while(self.running):
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glMatrixMode(GL_MODELVIEW)
            glPushMatrix()

            self.tick_and_render()

            glMatrixMode(GL_MODELVIEW)
            glPopMatrix()

            glfw.SwapBuffers()

    def update_layer(self, actor, layerIndex):
        self.deferred_layer_changes.append((actor, layerIndex))



world = World()
