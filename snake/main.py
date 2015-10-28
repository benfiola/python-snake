__author__ = 'Ben'

import os
import sys

os.environ["PYSDL2_DLL_PATH"] = "C:\\Users\\Ben\\PycharmProjects\\TetrisDemo\\third_party"

import sdl2
import sdl2.ext
from configuration import configuration
from game.Game import Game

def run():
    sdl2.ext.init()
    window = sdl2.ext.Window("Snake", size=(configuration.window_width, configuration.window_height))
    world = sdl2.ext.World()
    window.show()
    curr = Game(window, world)
    running = True
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
            curr.handle_event(event)
        world.process()
        if curr.game_state.game_over is True:
            curr.clean_up()
            curr = Game(window, world)
    return 0

if __name__ == "__main__":
    sys.exit(run())