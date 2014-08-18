__author__ = 'bdavis'

from infrastructure.color import Color
from OpenGL.GL import *
from infrastructure.vector2 import Vector2
from infrastructure.textures import get_texture_reference
from util import mathutil
import logging

logger = logging.getLogger()

MAX_SPRITE_FRAMES = 64

SQUARE_VERTS = [-0.5,  0.5, -0.5, -0.5, 0.5,  0.5, 0.5, -0.5]

num_actors = 0

class LoopAnimation(object):
    def __init__(self, startFrame, endFrame, delay):
        self.startFrame = startFrame
        self.endFrame = endFrame
        self.currentFrame = self.startFrame
        self.currentFrameDelay = delay
        self.frameDelay = delay

    def compute(self, dt):
        if self.frameDelay < 0:
            return 0

        self.currentFrameDelay -= dt

        if self.currentFrameDelay < 0:
            self.currentFrame += 1
            self.currentFrameDelay = self.frameDelay

        if self.currentFrame > self.endFrame:
            self.currentFrame = self.startFrame

        return self.currentFrame

class Actor(object):
    def __init__(self):
        self.size = Vector2(1.0,1.0)
        self.position = Vector2(0.0,0.0)
        self.color = Color()
        self._rotation = 0.0
        self._spriteTextureReferences = [0.0]*MAX_SPRITE_FRAMES
        self._spriteCurrentFrame = 0
        self._animation = None
        self._spriteNumFrames = 0
        self._uvs = [0.0] * 8
        self.set_uvs(Vector2(0.0,0.0), Vector2(1.0,1.0))

        global num_actors
        self.id = num_actors
        num_actors+=1




    def play_sprite_animation(self, delay, startFrame, endFrame):
        self._animation = LoopAnimation(startFrame, endFrame, delay)

    def update_sprite_animation(self, dt):
        if self._animation:
            self._spriteCurrentFrame = self._animation.compute(dt)

    def update(self, dt):
        self.update_sprite_animation(dt)


    def set_sprite_texture(self, textureReference, frame):
        frame = mathutil.clamp(frame, 0, MAX_SPRITE_FRAMES - 1)

        if (frame >= self._spriteNumFrames):
            self._spriteNumFrames = frame + 1;

        self._spriteTextureReferences[frame] = textureReference;

    def set_position(self, x, y):
        self.position.X = x
        self.position.Y = y

    def set_uvs(self, lowleft, upright):
        self._uvs[0] = lowleft.X
        self._uvs[1] = upright.Y
        self._uvs[2] = lowleft.X
        self._uvs[3] = lowleft.Y
        self._uvs[4] = upright.X
        self._uvs[5] = upright.Y
        self._uvs[6] = upright.X
        self._uvs[7] = lowleft.Y

    def load_sprite_frames(self, globPattern, clampmode = GL_CLAMP, filtermode = GL_LINEAR):
        import glob
        textures = glob.glob(globPattern+'*')
        textures.sort()
        for i, t in enumerate(textures):
            self.set_sprite(t, i, clampmode, filtermode)


    def set_size(self, x, y = 0.0):
        if type(x) == Vector2:
            self.size = x
        else:
            self.size = Vector2(x,y)


    def set_sprite(self, filename, frame=0, clampmode = GL_CLAMP, filtermode = GL_LINEAR):
        logger.debug('set_sprite {0} frame={1}'.format(filename, frame) )
        textureReference = get_texture_reference(filename, clampmode, filtermode)
        if textureReference == -1:
            return False

        self.set_sprite_texture(textureReference, frame)
        return True

    def render(self):
        glPushMatrix();
        glTranslatef(self.position.X, self.position.Y, 0.0);
        glRotatef(self._rotation, 0, 0, 1);
        glScalef(self.size.X, self.size.Y, 1.0);
        glColor4f(self.color.R, self.color.G, self.color.B, self.color.A);

        textureReference = self._spriteTextureReferences[self._spriteCurrentFrame];
        if (textureReference >= 0):
            glEnable(GL_TEXTURE_2D);
            glBindTexture(GL_TEXTURE_2D, textureReference);

        glEnableClientState(GL_VERTEX_ARRAY);
        glEnableClientState(GL_TEXTURE_COORD_ARRAY);
        glVertexPointer(2, GL_FLOAT, 0, SQUARE_VERTS);
        glTexCoordPointer(2, GL_FLOAT, 0, self._uvs);
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4);

        if (textureReference >= 0):
            glDisable(GL_TEXTURE_2D);

        glPopMatrix();


    rotation = property(lambda self: self._rotation)
