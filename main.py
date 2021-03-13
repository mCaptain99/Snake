import time

import pygame

from snake import Snake, Direction

segment_count = 20
segment_size = 20
board_size = segment_count * segment_size


def blit_snake(snake, screen, image):
    for segment in snake.body:
        x, y = segment.get_coordinates()
        screen.blit(image, (segment_size*x, segment_size*y))
    pygame.display.flip()


def blit_apple(apple, screen, image):
    screen.blit(image, (segment_size * apple[0], segment_size * apple[1]))
    pygame.display.flip()


def end_game(screen, result):
    while True:
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont(pygame.font.get_default_font(), 30)
        text = font.render('''End of game. Your result is {}. 
                            Press any key to close'''.format(result), False, (255, 255, 255))
        screen.blit(text, (20, board_size // 2))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                else:
                    main()


def main():
    pygame.init()
    screen = pygame.display.set_mode((board_size, board_size))
    running = True
    snake = Snake(10, 10, Direction.UP)
    image = pygame.image.load("img/board.png")
    while running:
        blit_snake(snake, screen, image)
        event = pygame.event.poll()
        if event and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.turn(Direction.UP)
            elif event.key == pygame.K_DOWN:
                snake.turn(Direction.DOWN)
            elif event.key == pygame.K_RIGHT:
                snake.turn(Direction.RIGHT)
            elif event.key == pygame.K_LEFT:
                snake.turn(Direction.LEFT)
        snake.move()
        screen.fill((0, 0, 0))
        blit_snake(snake, screen, image)
        blit_apple(snake.board.apple, screen, image)
        if snake.check_if_eaten():
            break
        time.sleep(0.1)
    end_game(screen, len(snake.body))


if __name__ == '__main__':
    main()
