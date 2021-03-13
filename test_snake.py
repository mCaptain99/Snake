import pytest

from snake import Direction, Snake, Segment


@pytest.fixture()
def snake():
    return Snake(10, 10, Direction.DOWN)


def test_enlarge(snake):
    for i in range(5):
        snake.move()
        snake.enlarge()
    for i, segment in enumerate(snake.body):
        assert segment.x == 10 and segment.y == 15-i and segment.direction == Direction.DOWN


def test_turn(snake):
    for i in range(2):
        snake.enlarge()
    assert snake.body == [Segment(10, 10, Direction.DOWN), Segment(10, 9, Direction.DOWN),
                          Segment(10, 8, Direction.DOWN)]
    snake.turn(Direction.RIGHT)
    assert snake.body == [Segment(10, 10, Direction.RIGHT), Segment(10, 9, Direction.DOWN),
                          Segment(10, 8, Direction.DOWN)]
    snake.move()
    assert snake.body == [Segment(11, 10, Direction.RIGHT), Segment(10, 10, Direction.RIGHT),
                          Segment(10, 9, Direction.DOWN)]
    snake.move()
    assert snake.body == [Segment(12, 10, Direction.RIGHT), Segment(11, 10, Direction.RIGHT),
                          Segment(10, 10, Direction.RIGHT)]
    snake.move()
    assert snake.body == [Segment(13, 10, Direction.RIGHT), Segment(12, 10, Direction.RIGHT),
                          Segment(11, 10, Direction.RIGHT)]


def test_eaten(snake):
    for i in range(9):
        snake.enlarge()
    snake.move()
    snake.turn(Direction.RIGHT)
    snake.move()
    snake.move()
    snake.turn(Direction.UP)
    snake.move()
    snake.move()
    snake.turn(Direction.LEFT)
    snake.move()
    snake.move()
    print(snake.body)
    assert snake.check_if_eaten()


def test_apple(snake):
    for i in range(15):
        snake.enlarge()
    for i in range(100):
        snake.board.random_apple(snake)
        assert snake.board.apple not in [segment.get_coordinates() for segment in snake.body]


def test_eat_apple(snake):
    for i in range(15):
        snake.enlarge()
    snake.board.apple = (10, 11)
    snake.move()
    assert len(snake.body) == 17