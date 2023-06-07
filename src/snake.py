import random

from collections import deque
from dataclasses import dataclass
from enum import Enum
from typing import Tuple


import pygame

COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_GREEN = (0, 255, 0)
COLOR_RED = (255, 0, 0)
COLOR_WHITE = (255, 255, 255)

GAME_NAME = "SNAKE by Frechousky"
GRID_SIZE = (16, 16)
CELL_WIDTH = CELL_HEIGHT = 16
WINDOW_SIZE = (GRID_SIZE[0] * CELL_HEIGHT, GRID_SIZE[1] * CELL_WIDTH)

FPS = 5

SNAKE_MAXLEN = GRID_SIZE[0] * GRID_SIZE[1]

TXT_GAME_OVER = "GAME OVER ! PRESS ANY KEY TO RESTART."
TXT_WIN = "CONGRATS YOU WON ! PRESS ANY KEY TO RESTART."


class GameState(Enum):
    STOP = 0
    RUNNING = 1
    GAME_OVER = 2
    WIN = 3


class Direction(Enum):
    TOP = 0
    RIGHT = 1
    BOTTOM = 2
    LEFT = 3


@dataclass
class Snake:
    direction: Direction
    body: deque


@dataclass
class GameData:
    state: GameState
    snake: Snake
    body_part_pos: Tuple[int, int] = None


def init_pygame() -> pygame.Surface:
    """intialize pygame"""
    pygame.init()
    pygame.mouse.set_visible(0)
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption(GAME_NAME)
    return screen


def generate_random_snake() -> Snake:
    """generate snake of size one, heading in random direction, at random position"""
    random.seed()
    direction = Direction(random.randint(0, 3))
    starting_pos = (
        random.randint(0, GRID_SIZE[0] - 1),
        random.randint(0, GRID_SIZE[1] - 1),
    )
    return Snake(
        direction,
        deque([starting_pos], maxlen=SNAKE_MAXLEN),
    )


def generate_random_body_part_pos(snake: Snake) -> Tuple[int, int]:
    """generate random position on grid where snake does not belong"""
    random.seed()
    is_valid_pos = False
    body_part_pos = None
    while not is_valid_pos:
        body_part_pos = (
            random.randint(0, GRID_SIZE[0] - 1),
            random.randint(0, GRID_SIZE[1] - 1),
        )
        is_valid_pos = not body_part_pos in snake.body
    return body_part_pos


def handle_inputs(data: GameData) -> None:
    """
    handle user inputs
    - ^ (top arrow): snake goes top
    - v (bottom arrow): snake goes bottom
    - < (left arrow): snake goes left
    - > (right arrow): snake goes right
    """
    curr_direction = data.snake.direction
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            data.state = GameState.STOP
            return
        if event.type == pygame.KEYDOWN:
            if data.state in [GameState.GAME_OVER, GameState.WIN]:
                data.snake = generate_random_snake()
                data.body_part_pos = generate_random_body_part_pos(data.snake)
                data.state = GameState.RUNNING
                return
            if event.key == pygame.K_UP and curr_direction != Direction.BOTTOM:
                data.snake.direction = Direction.TOP
            elif event.key == pygame.K_DOWN and curr_direction != Direction.TOP:
                data.snake.direction = Direction.BOTTOM
            elif event.key == pygame.K_LEFT and curr_direction != Direction.RIGHT:
                data.snake.direction = Direction.LEFT
            elif event.key == pygame.K_RIGHT and curr_direction != Direction.LEFT:
                data.snake.direction = Direction.RIGHT


def update(data: GameData) -> None:
    """update game data"""
    if data.state != GameState.RUNNING:
        return

    # update head
    head = data.snake.body.pop()
    data.snake.body.append(head)
    new_head_x, new_head_y = head
    if data.snake.direction == Direction.TOP:
        new_head_y = new_head_y - 1
    elif data.snake.direction == Direction.BOTTOM:
        new_head_y = new_head_y + 1
    elif data.snake.direction == Direction.LEFT:
        new_head_x = new_head_x - 1
    elif data.snake.direction == Direction.RIGHT:
        new_head_x = new_head_x + 1
    new_head = (new_head_x % GRID_SIZE[0], new_head_y % GRID_SIZE[1])
    if data.snake.body.count(new_head) > 0:
        # snake heads in itself
        data.state = GameState.GAME_OVER
        return
    data.snake.body.append(new_head)

    if new_head != data.body_part_pos:
        # remove tail
        data.snake.body.popleft()
    else:
        if len(data.snake.body) == SNAKE_MAXLEN:
            data.state = GameState.WIN
            return
        # snake gets new body part
        # generate new body part on map
        data.body_part_pos = generate_random_body_part_pos(data.snake)


def blit_centered_text_msg(
    txt: str, color: Tuple[int, int, int], screen: pygame.Surface
):
    f = pygame.font.Font(None, 16)
    s = f.render(txt, False, color)
    pos = (
        (WINDOW_SIZE[0] - s.get_rect().width) / 2,
        (WINDOW_SIZE[1] - s.get_rect().height) / 2,
    )
    screen.blit(s, pos)


def render(data: GameData, screen: pygame.Surface) -> None:
    """render GUI"""
    screen.fill(COLOR_BLACK)

    # draw snake
    for snake_body_part in data.snake.body:
        x, y = snake_body_part
        pygame.draw.rect(
            surface=screen,
            color=COLOR_WHITE,
            rect=pygame.Rect(
                (x * CELL_WIDTH, y * CELL_HEIGHT), (CELL_WIDTH, CELL_HEIGHT)
            ),
        )

    # draw body part to collect
    x, y = data.body_part_pos
    pygame.draw.rect(
        surface=screen,
        color=COLOR_BLUE,
        rect=pygame.Rect((x * CELL_WIDTH, y * CELL_HEIGHT), (CELL_WIDTH, CELL_HEIGHT)),
    )

    if data.state == GameState.GAME_OVER:
        blit_centered_text_msg(TXT_GAME_OVER, COLOR_RED, screen)

    elif data.state == GameState.WIN:
        blit_centered_text_msg(TXT_WIN, COLOR_GREEN, screen)

    pygame.display.update()


def run() -> None:
    """run game"""
    screen = init_pygame()
    clock = pygame.time.Clock()
    snake = generate_random_snake()
    data = GameData(GameState.RUNNING, snake, generate_random_body_part_pos(snake))
    while data.state != GameState.STOP:
        clock.tick(FPS)
        handle_inputs(data)
        update(data)
        render(data, screen)


if __name__ == "__main__":
    run()
