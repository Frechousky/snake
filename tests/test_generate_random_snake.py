from snake import GRID_SIZE, Direction, generate_random_snake


def test__snakes_are_valid():
    for _ in range(1000):
        snake = generate_random_snake()
        snake_pos = snake.body.pop()
        assert snake.direction in Direction
        assert snake_pos[0] in range(GRID_SIZE[0])
        assert snake_pos[1] in range(GRID_SIZE[1])
