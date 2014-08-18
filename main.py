__author__ = 'bdavis'

from infrastructure.world import world
from actors.actor import Actor

world.initialize(1024,768, "Warsong Redux", True, False, True);
import os

import inspect, os
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

#print inspect.getfile(inspect.currentframe()) # script filename (usually with path)
dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory
os.chdir(dir)

import client_game

client_game.initialize()

world.start()

