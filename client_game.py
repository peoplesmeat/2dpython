__author__ = 'bdavis'

from infrastructure.world import world
from actors.actor import Actor
from random import randint
from infrastructure.vector3 import Vector3
from infrastructure.camera import camera
from infrastructure.textures import open_image, merge_images

class Tile(object):
    def __init__(self, x, y, sprite):
        self.actor = Actor()
        self.actor.set_position(x,y)
        self.actor.set_sprite(sprite)
        world.add(self.actor)

class Board(object):
    def __init__(self, height, width):

        tile_names = ["Resources/images/roadA.png", "Resources/images/treesA.png", "Resources/images/grassA.png"]

        self.height = height
        self.width = width
        tiles = [ 0 ] * self.width
        for i in range(0, self.width):
            tiles[i] = [ 0 ] * self.height
            for j in range(0, self.height):
                tiles[i][j] = open_image(tile_names[randint(0,2)])
        board_texture = merge_images(tiles)
        board_actor = Actor()
        board_actor.set_sprite(board_texture)
                #tiles[i][j] = Tile(i, j, tile_names[randint(0,2)])


def initialize():

    camera.position = Vector3(0.0,0.0,5.0)

    board = Board(30,25)

    cursor = Actor()
    cursor.set_position(3,3)
    cursor.set_size(1.25)
    world.update_layer(cursor, 5)
    cursor.set_sprite("Resources/Images/cursor.png")

    soldier = Actor()
    soldier.load_sprite_frames("Resources/Images/soldierA")
    soldier.set_size(1.0,1.0)
    soldier.set_position(3.0,3.0)
    soldier.play_sprite_animation(1.0, 0, 1)
    world.add(soldier)

    count = Actor()
    count.set_position(3.0,3.0)
    count.set_sprite("Resources/Images/10.png")
    world.add(count)
