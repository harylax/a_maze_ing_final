def embed_42(
        grid_visited: list[list[bool]],
        width: int,
        height: int
        ) -> list[tuple[int, int]]:
    if width < 9 or height < 7:
        print("Maze is too small for the pattern 42")
        return []
    schema: list[list[int]] = [
        [1, 0, 0, 0, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 1],
        [0, 0, 1, 0, 1, 0, 0],
        [0, 0, 1, 0, 1, 1, 1],
    ]
    cx, cy = width // 2, height // 2
    x, y = cx - 3, cy - 2
    result_42: list[tuple[int, int]] = []
    for j, row in enumerate(schema):
        for i, element in enumerate(row):
            if element == 1:
                result_42.append((i + x, j + y))
                grid_visited[j + y][i + x] = True
    return result_42
