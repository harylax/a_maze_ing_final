import random
from .pattern_42 import embed_42
from .solver import bfs
import sys

class MazeGenerator:
    def __init__(
            self,
            width: int = 30,
            height: int = 30,
            entry: tuple[int, int] = (1, 1),
            exit_: tuple[int, int] = (23, 25),
            output_file: str = "",
            perfect: bool = True,
            seed: int = 42
    ) -> None:
        self.width: int = width
        self.height: int = height
        self.entry: tuple[int, int] = entry
        self.exit_: tuple[int, int] = exit_
        self.output_file: str = output_file
        self.perfect: bool = perfect
        self.grid: list[list[int]] = []
        self.grid_visited: list[list[bool]] = []
        self.result: list[tuple[int, int]] = []
        self.pattern_42: list[tuple[int, int]] = []
        self.seed: int = seed
        self.history: list[tuple[int, int]] = [entry]

    def generate(self) -> None:
        sys.setrecursionlimit(100000)
        random.seed(self.seed)
        self.fill_grid()
        self.pattern_42 = embed_42(self.grid_visited, self.width, self.height)
        self.dfs(self.entry[0], self.entry[1])
        self.result = bfs(self.entry, self.exit_, self.grid, self.width, self.height)

    def fill_grid(self) -> None:
        for _ in range(self.height):
            row: list[int] = []
            row_visited: list[bool] = []
            for _ in range(self.width):
                row.append(15)
                row_visited.append(False)
            self.grid.append(row)
            self.grid_visited.append(row_visited)

    def dfs(self, x: int, y: int) -> None:
        if self.entry not in self.history:
            self.history.append(self.entry)
        directions: list[tuple[int, int]] = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if nx < self.width and ny < self.height and nx >= 0 and ny >= 0 and not self.grid_visited[ny][nx]:
                self.grid_visited[ny][nx] = True
                if nx > x:
                    self.grid[ny][nx] = self.grid[ny][nx] & ~ 8
                    self.grid[y][x] = self.grid[y][x] & ~ 2
                if nx < x:
                    self.grid[ny][nx] = self.grid[ny][nx] & ~ 2
                    self.grid[y][x] = self.grid[y][x] & ~ 8
                if ny > y:
                    self.grid[ny][nx] = self.grid[ny][nx] & ~ 1
                    self.grid[y][x] = self.grid[y][x] & ~ 4
                if ny < y:
                    self.grid[ny][nx] = self.grid[ny][nx] & ~ 4
                    self.grid[y][x] = self.grid[y][x] & ~ 1

                self.history.append((nx, ny))
                self.dfs(nx, ny)

    def result_path(self) -> str:
        result: str = ""
        for i in range(1, len(self.result)):
            x, y = self.result[i - 1]
            nx, ny = self.result[i]
            if nx > x:
                result += 'E'
            elif nx < x:
                result += 'W'
            elif ny > y:
                result += 'S'
            elif ny < y:
                result += 'N'
        return result


if __name__ == "__main__":
    mg = MazeGenerator()
    mg.fill_grid()

    # for i in range(10):
    # 	print(f"{mg.grid[i]}")
    mg.generate()

    for i in range(10):
        print(f"{mg.grid[i]}")

    # output = "\n".join("".join(format(cell, "X") for cell in row) for row in mg.grid)
    # print(f"\noutput: \n{output}")

    print("\nResult: ")
    print(f"{mg.result}")