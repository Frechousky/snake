from collections import deque
from typing import List, Tuple

import pytest

from snake import GRID_SIZE, Direction, GameData, GameState, Snake, update


@pytest.mark.parametrize(
    "direction,snake_body_pos,expected_head_pos",
    [
        (Direction.TOP, [(0, 0), (0, 1), (1, 1)], (1, 0)),
        (Direction.RIGHT, [(0, 0), (0, 1), (1, 1)], (2, 1)),
        (Direction.BOTTOM, [(0, 0), (0, 1), (1, 1)], (1, 2)),
        (Direction.LEFT, [(0, 0), (1, 0), (1, 1)], (0, 1)),
    ],
)
def test__updates_snake_head(
    direction: Direction,
    snake_body_pos: List[Tuple[int, int]],
    expected_head_pos: Tuple[int, int],
):
    data = GameData(GameState.RUNNING, Snake(direction, deque(snake_body_pos)))

    update(data)

    assert data.snake.body.pop() == expected_head_pos


@pytest.mark.parametrize(
    "direction,snake_body_pos,expected_tail_pos",
    [
        (Direction.TOP, [(0, 0), (0, 1), (1, 1)], (0, 1)),
        (Direction.RIGHT, [(0, 0), (0, 1), (1, 1)], (0, 1)),
        (Direction.BOTTOM, [(0, 0), (0, 1), (1, 1)], (0, 1)),
        (Direction.LEFT, [(0, 0), (1, 0), (1, 1)], (1, 0)),
    ],
)
def test__removes_snake_tail(
    direction: Direction,
    snake_body_pos: List[Tuple[int, int]],
    expected_tail_pos: Tuple[int, int],
):
    data = GameData(GameState.RUNNING, Snake(direction, deque(snake_body_pos)))

    update(data)

    assert data.snake.body.popleft() == expected_tail_pos


@pytest.mark.parametrize(
    "direction,snake_body_pos,expected_head_pos",
    [
        (Direction.TOP, [(9, 0)], (9, GRID_SIZE[1] - 1)),
        (Direction.RIGHT, [(GRID_SIZE[0] - 1, 0)], (0, 0)),
        (Direction.BOTTOM, [(1, GRID_SIZE[1] - 1)], (1, 0)),
        (Direction.LEFT, [(0, 14)], (GRID_SIZE[0] - 1, 14)),
    ],
)
def test__when_snake_head_hits_corner__pops_on_opposite_side(
    direction: Direction,
    snake_body_pos: List[Tuple[int, int]],
    expected_head_pos: Tuple[int, int],
):
    data = GameData(GameState.RUNNING, Snake(direction, deque(snake_body_pos)))

    update(data)

    assert data.snake.body.pop() == expected_head_pos


PARAMS = [
    (Direction.TOP, [(1, 1)], (1, 0)),
    (Direction.RIGHT, [(1, 1)], (2, 1)),
    (Direction.BOTTOM, [(1, 1)], (1, 2)),
    (Direction.LEFT, [(1, 1)], (0, 1)),
    (Direction.TOP, [(7, 0)], (7, GRID_SIZE[1] - 1)),
    (Direction.RIGHT, [(GRID_SIZE[0] - 1, 6)], (0, 6)),
    (Direction.BOTTOM, [(12, GRID_SIZE[1] - 1)], (12, 0)),
    (Direction.LEFT, [(0, 11)], (GRID_SIZE[0] - 1, 11)),
]


@pytest.mark.parametrize("direction,snake_body_pos,body_part_pos", PARAMS)
def test__when_snake_head_hits_new_body_part__updates_snake_length_by_1(
    direction: Direction,
    snake_body_pos: List[Tuple[int, int]],
    body_part_pos: Tuple[int, int],
):
    data = GameData(
        GameState.RUNNING, Snake(direction, deque(snake_body_pos)), body_part_pos
    )

    len_before = len(data.snake.body)

    update(data)

    len_after = len(data.snake.body)

    assert len_after == len_before + 1, "snake length updates by 1"


@pytest.mark.parametrize("direction,snake_body_pos,body_part_pos", PARAMS)
def test__when_snake_head_hits_new_body_part__queue_is_not_removed(
    direction: Direction,
    snake_body_pos: List[Tuple[int, int]],
    body_part_pos: Tuple[int, int],
):
    data = GameData(
        GameState.RUNNING, Snake(direction, deque(snake_body_pos)), body_part_pos
    )

    queue_before = data.snake.body.popleft()
    data.snake.body.appendleft(queue_before)

    update(data)

    queue_after = data.snake.body.popleft()
    data.snake.body.appendleft(queue_after)

    assert queue_after == queue_before, "queue is not removed"


@pytest.mark.parametrize("direction,snake_body_pos,body_part_pos", PARAMS)
def test__when_snake_head_hits_new_body_part__new_body_part_spawns(
    direction: Direction,
    snake_body_pos: List[Tuple[int, int]],
    body_part_pos: Tuple[int, int],
):
    data = GameData(
        GameState.RUNNING, Snake(direction, deque(snake_body_pos)), body_part_pos
    )

    update(data)

    assert body_part_pos != data.body_part_pos, "new body part spawns"


# TODO
# def test__when_collecting_last_snake_part__game_is_won():
#     data = GameData(GameState.RUNNING, Snake(Direction.BOTTOM, deque([(0, 0)])), None)

#     update(data)

#     assert data.state == GameState.WIN
