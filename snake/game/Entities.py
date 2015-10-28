__author__ = 'Ben'

from snake.configuration import configuration, colors
from collections import deque
import sdl2
import sdl2.ext

class BlockList(object):
    def __init__(self, world, init_block):
        self.blocks = deque()
        self.blocks.append(init_block)


class GameState(object):
    def __init__(self):
        self.game_over = False


class BoardPosition(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.x == other.x and self.y == other.y

    def __neq__(self, other):
        return not isinstance(other, self.__class__) or self.x != other.x or self.y != other.y

    def pos_left(self):
        x = self.x - 1
        if x < 0:
            x = configuration.board_width-1
        return BoardPosition(x, self.y)

    def pos_right(self):
        x = self.x + 1
        if x >= configuration.board_width:
            x = 0
        return BoardPosition(x, self.y)

    def pos_up(self):
        y = self.y - 1
        if y < 0:
            y = configuration.board_height - 1
        return BoardPosition(self.x, y)

    def pos_down(self):
        y = self.y + 1
        if y >= configuration.board_height:
            y = 0
        return BoardPosition(self.x, y)

class EmptyBag(object):
    def __init__(self):
        pass


class Board(object):
    def __init__(self):
        self.spaces = [[None for y in range(configuration.board_height)] for x in range(configuration.board_width)]
        self.apple = None

class Direction(object):
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3

    def __init__(self):
        self.direction = Direction.LEFT


class InputData(object):
    def __init__(self):
        self.up = None
        self.down = None
        self.left = None
        self.right = None
        self.reset()

    def reset(self):
        self.up = False
        self.down = False
        self.left = False
        self.right = False


class Block(sdl2.ext.Entity):
    def __init__(self, world, board_position, color):
        self.boardposition = board_position
        factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
        self.color = color
        self.sprite = factory.from_color(colors.BLACK, size=(configuration.block_width, configuration.block_height))
        sdl2.ext.fill(self.sprite, self.color, (1, 1, configuration.block_width-2, configuration.block_height-2))
        self.recalculate_sprite_position()

    def recalculate_sprite_position(self):
        self.sprite.position = (configuration.block_width * self.boardposition.x, configuration.block_height * self.boardposition.y)

class Apple(Block):
    def __init__(self, world, board_position):
        super(Apple, self).__init__(world, board_position, colors.RED)


class BoardData(sdl2.ext.Entity):
    def __init__(self, world):
        self.board = Board()
        self.emptybag = EmptyBag()


class Snake(sdl2.ext.Entity):
    def __init__(self, world, input_data, board):
        init_pos = BoardPosition(configuration.board_width/2, configuration.board_height/2)
        block = Block(world, init_pos, colors.WHITE)

        self.blocklist = BlockList(world, block)
        self.direction = Direction()
        self.inputdata = input_data
        self.emptybag = EmptyBag()
        self.board = board




