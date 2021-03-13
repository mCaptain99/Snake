from enum import Enum
import random


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    RIGHT = (1, 0)
    LEFT = (-1, 0)


class Board:
    def __init__(self, sx, sy):
        self.sx = sx
        self.sy = sy
        self.apple = None

    def random_apple(self, snake):
        while True:
            x = random.randint(0, self.sx-1)
            y = random.randint(0, self.sy-1)
            if (x, y) not in [segment.get_coordinates() for segment in snake.body]:
                self.apple = (x, y)
                break



default_board = Board(20, 20)


class Segment:
    def __init__(self, x, y, direction, board=default_board):
        self.x = x
        self.y = y
        self.direction = direction
        self.board = board

    def move(self):
        x, y = self.direction.value
        self.x = (self.x + x) % self.board.sx
        self.y = (self.y + y) % self.board.sy

    def __eq__(self, other):
        if isinstance(other, Segment):
            return self.x == other.x and self.y == other.y and self.direction == other.direction
        else:
            raise NotImplemented

    def __repr__(self):
        return "(" + str(self.x) + " " + str(self.y) + " " + str(self.direction) + ")"

    def get_coordinates(self):
        return self.x, self.y


class Snake:
    def __init__(self, start_x, start_y, direction, board=default_board):
        self.body = [Segment(start_x, start_y, direction)]
        self.head = self.body[0]
        self.board = board

    def turn(self, direction):
        x, y = self.head.direction.value
        dx, dy = direction.value
        if x + dx or y + dy:
            self.head.direction = direction

    def move(self):
        for segment in self.body:
            segment.move()
        self.update_directions()
        self.check_if_apple()

    def update_directions(self):
        length = len(self.body)
        inverted_body = self.body[::-1]
        for i, segment in enumerate(inverted_body):
            if i != length - 1:
                prev = inverted_body[i+1]
                segment.direction = prev.direction

    def enlarge(self):
        tail = self.body[-1]
        dir_x, dir_y = tail.direction.value
        self.body.append(Segment(tail.x - dir_x, tail.y - dir_y, tail.direction))

    def check_if_eaten(self):
        head_coordinates = self.head.get_coordinates()
        return head_coordinates in [(segment.x, segment.y) for segment in self.body[1:]]

    def check_if_apple(self):
        if not self.board.apple:
            self.board.random_apple(self)
        elif self.board.apple == self.head.get_coordinates():
            self.enlarge()
            self.board.random_apple(self)
