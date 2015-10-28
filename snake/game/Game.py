__author__ = 'Ben'
import sdl2
import sdl2.ext
import datetime
import random
from snake.configuration import colors
from snake.game.Entities import *


class Renderer(sdl2.ext.SoftwareSpriteRenderSystem):
    def __init__(self, window):
        super(Renderer, self).__init__(window)

    def render(self, components, x=None, y=None):
        sdl2.ext.fill(self.surface, colors.BLACK)
        super(Renderer, self).render(components)

class MovementSystem(sdl2.ext.Applicator):
    def __init__(self, game_state):
        super(MovementSystem, self).__init__()
        self.game_state = game_state
        self.componenttypes = BlockList, Direction, InputData, Board
        self.last_move = datetime.datetime.now()
        self.move_timer = 100*1000

    def process(self, world, componentsets):
        curr_time = datetime.datetime.now()
        for blocklist, direction, inputdata, board in componentsets:
            if inputdata.up and direction.direction is not Direction.DOWN:
                direction.direction = Direction.UP
            elif inputdata.down and direction.direction is not Direction.UP:
                direction.direction = Direction.DOWN
            elif inputdata.left and direction.direction is not Direction.RIGHT:
                direction.direction = Direction.LEFT
            elif inputdata.right and direction.direction is not Direction.LEFT:
                direction.direction = Direction.RIGHT

            inputdata.reset()

            if (curr_time - self.last_move).microseconds > self.move_timer:
                self.last_move = curr_time

                # we're moving
                # if the block we're moving to is an apple, make a new block on that apple
                head = blocklist.blocks.popleft()
                head_pos = head.boardposition
                blocklist.blocks.appendleft(head)
                next_pos = None
                if direction.direction is Direction.UP:
                    next_pos = head_pos.pos_up()
                elif direction.direction is Direction.DOWN:
                    next_pos = head_pos.pos_down()
                elif direction.direction is Direction.LEFT:
                    next_pos = head_pos.pos_left()
                elif direction.direction is Direction.RIGHT:
                    next_pos = head_pos.pos_right()

                if board.apple.boardposition == next_pos:
                    world.delete(board.apple)
                    board.apple = None
                    new_block = Block(world, next_pos, colors.WHITE)
                    board.spaces[next_pos.x][next_pos.y] = new_block
                    blocklist.blocks.appendleft(new_block)
                    new_block.recalculate_sprite_position()
                    self.move_timer = self.move_timer - 2000
                elif board.spaces[next_pos.x][next_pos.y] is not None:
                    self.game_state.game_over = True
                else:
                    curr_block = blocklist.blocks.pop()
                    old_pos = curr_block.boardposition
                    board.spaces[old_pos.x][old_pos.y] = None
                    curr_block.boardposition = next_pos
                    board.spaces[next_pos.x][next_pos.y] = curr_block
                    blocklist.blocks.appendleft(curr_block)
                    curr_block.recalculate_sprite_position()


class AppleSpawner(sdl2.ext.Applicator):
    def __init__(self):
        super(AppleSpawner, self).__init__()
        self.componenttypes = Board, EmptyBag

    def process(self, world, componentsets):
        for board, empty_bag in componentsets:
            if board.apple is None:
                x = random.randrange(len(board.spaces))
                y = random.randrange(len(board.spaces[x]))
                while board.spaces[x][y] is not None:
                    x = random.randrange(len(board.spaces))
                    y = random.randrange(len(board.spaces[x]))
                board.apple = Apple(world, BoardPosition(x, y))
                board.spaces[x][y] = board.apple


class Game(object):
    def __init__(self, window, world):
        self.window = window
        self.world = world
        self.input_data = InputData()
        self.game_state = GameState()
        self.world.add_system(AppleSpawner())
        self.world.add_system(MovementSystem(self.game_state))
        self.world.add_system(Renderer(window))
        bd = BoardData(self.world)
        Snake(self.world, self.input_data, bd.board)

    def handle_event(self, event):
         if event.key.keysym.sym == sdl2.SDLK_DOWN:
            self.input_data.down = True
         elif event.key.keysym.sym == sdl2.SDLK_RIGHT:
            self.input_data.right = True
         elif event.key.keysym.sym == sdl2.SDLK_LEFT:
            self.input_data.left = True
         elif event.key.keysym.sym == sdl2.SDLK_UP:
            self.input_data.up = True

    def clean_up(self):
        while self.world.entities:
            entity = self.world.entities.pop()
            self.world.delete(entity)
        for system in self.world.systems:
            self.world.remove_system(system)


