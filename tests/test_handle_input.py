from typing import List
import pygame
import pytest

from snake import Direction, handle_inputs, GameData, GameState, Snake


@pytest.mark.parametrize("state", [gs for gs in GameState])
def test__on_quit__sets_game_state_to_stop(mocker, state: GameState):
    data = GameData(state, Snake(Direction.TOP, None))

    mocker.patch("pygame.event.get", return_value=[pygame.event.Event(pygame.QUIT)])

    handle_inputs(data)

    assert data.state == GameState.STOP


@pytest.mark.parametrize(
    "in_direction,key,out_direction",
    [
        # up arrow
        (Direction.TOP, pygame.K_UP, Direction.TOP),
        (Direction.RIGHT, pygame.K_UP, Direction.TOP),
        (Direction.LEFT, pygame.K_UP, Direction.TOP),
        # right arrow
        (Direction.TOP, pygame.K_RIGHT, Direction.RIGHT),
        (Direction.RIGHT, pygame.K_RIGHT, Direction.RIGHT),
        (Direction.BOTTOM, pygame.K_RIGHT, Direction.RIGHT),
        # bottom arrow
        (Direction.RIGHT, pygame.K_DOWN, Direction.BOTTOM),
        (Direction.BOTTOM, pygame.K_DOWN, Direction.BOTTOM),
        (Direction.LEFT, pygame.K_DOWN, Direction.BOTTOM),
        # left arrow
        (Direction.TOP, pygame.K_LEFT, Direction.LEFT),
        (Direction.BOTTOM, pygame.K_LEFT, Direction.LEFT),
        (Direction.LEFT, pygame.K_LEFT, Direction.LEFT),
    ],
)
def test__on_key_arrow_press__updates_snake_direction(
    mocker, in_direction: Direction, key: int, out_direction: Direction
):
    data = GameData(GameState.RUNNING, Snake(in_direction, None))

    mocker.patch(
        "pygame.event.get",
        return_value=[pygame.event.Event(pygame.KEYDOWN, {"key": key})],
    )

    handle_inputs(data)

    assert data.snake.direction == out_direction


@pytest.mark.parametrize(
    "in_direction,key,out_direction",
    [
        (Direction.BOTTOM, pygame.K_UP, Direction.BOTTOM),
        (Direction.LEFT, pygame.K_RIGHT, Direction.LEFT),
        (Direction.TOP, pygame.K_DOWN, Direction.TOP),
        (Direction.RIGHT, pygame.K_LEFT, Direction.RIGHT),
    ],
)
def test__on_key_arrow_press__does_not_update_snake_direction_into_opposite_direction(
    mocker, in_direction: Direction, key: int, out_direction: Direction
):
    data = GameData(GameState.RUNNING, Snake(in_direction, None))

    mocker.patch(
        "pygame.event.get",
        return_value=[pygame.event.Event(pygame.KEYDOWN, {"key": key})],
    )

    handle_inputs(data)

    assert data.snake.direction == out_direction


@pytest.mark.parametrize(
    "key,state",
    [
        (pygame.K_KP_ENTER, GameState.GAME_OVER),
        (pygame.K_SPACE, GameState.GAME_OVER),
        (pygame.K_r, GameState.GAME_OVER),
        (pygame.K_KP_ENTER, GameState.WIN),
        (pygame.K_SPACE, GameState.WIN),
        (pygame.K_r, GameState.WIN),
    ],
)
def test__when_game_over_or_game_win__on_any_key_press__restarts_game(
    mocker, state: GameState, key: int
):
    snake = Snake(Direction.TOP, None)
    body_part_pos = (-1, -1)
    data = GameData(state, snake, body_part_pos)

    mocker.patch(
        "pygame.event.get",
        return_value=[pygame.event.Event(pygame.KEYDOWN, {"key": key})],
    )

    handle_inputs(data)

    assert data.state == GameState.RUNNING
    assert data.snake != snake
    assert data.body_part_pos != body_part_pos


@pytest.mark.parametrize(
    "in_direction,keys,out_direction",
    [
        (Direction.BOTTOM, [pygame.K_RIGHT, pygame.K_UP], Direction.RIGHT),
        (Direction.LEFT, [pygame.K_DOWN, pygame.K_RIGHT], Direction.BOTTOM),
        (Direction.TOP, [pygame.K_LEFT, pygame.K_DOWN], Direction.LEFT),
        (Direction.RIGHT, [pygame.K_UP, pygame.K_LEFT], Direction.TOP),
        (
            Direction.BOTTOM,
            [
                pygame.K_RIGHT,
                pygame.K_UP,
                pygame.K_LEFT,
                pygame.K_UP,
            ],
            Direction.LEFT,
        ),
    ],
)
def test__on_successive_key_arrow_press__does_not_update_snake_direction_into_opposite_direction(
    mocker,
    in_direction: Direction,
    keys: List[int],
    out_direction: Direction,
):
    data = GameData(GameState.RUNNING, Snake(in_direction, None))

    mocker.patch(
        "pygame.event.get",
        return_value=[pygame.event.Event(pygame.KEYDOWN, {"key": key}) for key in keys],
    )

    handle_inputs(data)

    assert data.snake.direction == out_direction
