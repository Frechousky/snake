from collections import deque
from typing import List, Tuple

import pytest
from snake import GRID_SIZE, Direction, Snake, generate_random_body_part_pos

ALL_POS_EXPECT_9_9 = [
    (x, y) for x in range(GRID_SIZE[0]) for y in range(GRID_SIZE[1]) if (x, y) != (9, 9)
]


@pytest.mark.parametrize(
    "direction,snake_body_pos",
    [
        (Direction.TOP, [(0, 0)]),
        (Direction.RIGHT, [(2, 3)]),
        (Direction.BOTTOM, [(9, 8)]),
        (Direction.LEFT, [(12, 0)]),
        (Direction.TOP, ALL_POS_EXPECT_9_9),
    ],
)
def test__body_part_does_not_belong_to_snake__and_body_part_is_in_grid(
    direction: Direction,
    snake_body_pos: List[Tuple[int, int]],
):
    snake = Snake(direction, deque(snake_body_pos))
    for _ in range(100):
        body_part_pos = generate_random_body_part_pos(snake)
        assert body_part_pos not in snake.body
        assert 0 <= body_part_pos[0] < GRID_SIZE[0]
        assert 0 <= body_part_pos[1] < GRID_SIZE[1]
