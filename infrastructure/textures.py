__author__ = 'bdavis'

from OpenGL.GL import *

try:
    from PIL import Image
except ImportError, err:
    from Image import open

textureCache = {}


def open_image(image):
    return Image.open(image)

def merge_images(images):
    width, height = images[0][0].size

    im = Image.new("RGBA", (len(images[0])*width, len(images)*height) )
    x=0
    y=0
    for i in images:
        for j in i:
            im.paste(j, (x,y))
            x += j.size[0]
            y += j.size[1]

    return im

def get_texture_reference(image, clampMode, filterMode):

    if (type(image) == str):
        filename = image
        if (textureCache.has_key(filename)):
            return textureCache[filename]

        im = Image.open(filename)
    else:
        im = image
        filename = 'random'

    try:
        ix, iy, image = im.size[0], im.size[1], im.tostring("raw", "RGBA", 0, -1)
    except SystemError:
        ix, iy, image = im.size[0], im.size[1], im.tostring("raw", "RGBX", 0, -1)

    ID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, ID)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, clampMode);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, clampMode);

    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, filterMode);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, filterMode);

    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexImage2D(
        GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0,
        GL_RGBA, GL_UNSIGNED_BYTE, image
    )
    textureCache[filename] = ID
    return ID