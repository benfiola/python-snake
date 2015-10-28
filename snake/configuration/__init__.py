__author__ = 'Ben'
import sdl2.ext


class Configuration(object):
    def __init__(self):
        self.window_width = 800
        self.window_height = 600
        self.board_width = 40
        self.board_height = 30
        self.block_width = None
        self.block_height = None
        self.recalculate()

    def recalculate(self):
        self.block_width = self.window_width/self.board_width
        self.block_height = self.window_height/self.board_height


class Colors(object):
    def __init__(self):
        self.WHITE = sdl2.ext.Color(255, 255, 255)
        self.RED = sdl2.ext.Color(255, 0, 0)
        self.GREEN = sdl2.ext.Color(0, 255, 0)
        self.BLUE = sdl2.ext.Color(0, 0, 255)
        self.BLACK = sdl2.ext.Color(0, 0, 0)

configuration = Configuration()
colors = Colors()