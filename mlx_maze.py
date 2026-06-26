from mlx import Mlx
from maze.generator import MazeGenerator
from typing import Any


class MlxMaze:
    def __init__(self, maze_gen: MazeGenerator) -> None:
        self.width: int = maze_gen.width
        self.height: int = maze_gen.height
        self.entry: tuple[int, int] = maze_gen.entry
        self.exit_: tuple[int, int] = maze_gen.exit_
        self.grid: list[list[int]] = maze_gen.grid
        self.result: list[tuple[int, int]] = maze_gen.result
        self.pattern_42: list[tuple[int, int]] = maze_gen.pattern_42
        self.history: list[tuple[int, int]] = maze_gen.history
        self.mlx_maze: Mlx = Mlx()
        self.mlx_ptr: Any = self.mlx_maze.mlx_init()
        self.cell_size: int = self.compute_cell_size()
        self.win_width: int = \
            self.cell_size * self.width + self.cell_size // 10
        self.win_height: int = \
            self.cell_size * self.height + self.cell_size // 10
        self.win_ptr: Any = self.mlx_maze.mlx_new_window(
            self.mlx_ptr, self.win_width, self.win_height, 'Amazing'
            )
        self.is_touch_p: bool = False
        self.path_animation_index: int = 0
        self.maze_animation_index: int = 0
        self.pattern_animation_index: int = 0
        self.position: tuple[int, int] = self.entry
        self.wall_colors: list[int] = [
            0xFFFFFFFF,
            0xFFFFFF00,
            0xFFFF0000,
            0xFFFF00FF,
            0xFF00FFFF
        ]

    def compute_cell_size(self) -> int:
        min_cell_size: int = 10
        _, w_screen, h_screen = self.mlx_maze.mlx_get_screen_size(self.mlx_ptr)
        if min_cell_size * self.width > w_screen \
                or min_cell_size * self.height > h_screen:
            print(
                f"{self.width} x {self.height} exceed screen size; "
                f"max: {w_screen // min_cell_size} "
                f"x {h_screen // min_cell_size}"
                )
            exit(1)
        return max(
            min_cell_size,
            min(w_screen // self.width, h_screen // self.height)
            )

    def draw_rectangle(self, x: int, y: int, w: int, h: int, color: int) -> None:
        for j in range(y, y + h):
            for i in range(x, x + w):
                self.mlx_maze.mlx_pixel_put(
                    self.mlx_ptr,
                    self.win_ptr,
                    i, j, color
                    )

    def draw_cell(self, x: int, y: int, wall_value: int, color: int) -> None:
        wall_size = self.cell_size // 10
        px = x * self.cell_size
        py = y * self.cell_size

        if wall_value == 15:
            self.draw_rectangle(
                px, py,
                self.cell_size,
                self.cell_size,
                0XFFFF0099
                )
            return

        if wall_value & 1 == 1:
            self.draw_rectangle(px, py, self.cell_size, wall_size, color)
        if wall_value & 2 == 2 and wall_value & 4 == 4:
            self.draw_rectangle(
                px + self.cell_size, py,
                wall_size, self.cell_size + wall_size,
                color
                )
        elif wall_value & 2 == 2:
            self.draw_rectangle(
                px + self.cell_size, py, wall_size, self.cell_size, color
                )
        if wall_value & 4 == 4:
            self.draw_rectangle(
                px,  py + self.cell_size, self.cell_size, wall_size, color
                )
        if wall_value & 8 == 8:
            self.draw_rectangle(px,  py, wall_size, self.cell_size, color)

    def draw_maze(self) -> None:
        for j in range(self.height):
            for i in range(self.width):
                element = self.grid[j][i]
                self.draw_cell(i, j, element, self.wall_colors[0])
        self.draw_entry()
        self.draw_exit()

    def draw_entry(self) -> None:
        x, y = self.entry
        self.draw_rectangle(
            x * self.cell_size, y * self.cell_size,
            self.cell_size, self.cell_size,
            0xFF60A5FA
            )

    def draw_exit(self) -> None:
        x, y = self.exit_
        self.draw_rectangle(
            x * self.cell_size, y * self.cell_size,
            self.cell_size, self.cell_size,
            0xFFFB7185
            )

    def draw_path(self) -> None:
        for x, y in self.result:
            px = x * self.cell_size
            py = y * self.cell_size
            if (x, y) in [self.entry, self.exit_]:
                continue
            self.draw_rectangle(
                px, py, self.cell_size, self.cell_size, 0XFF22C55E
                )
            self.draw_cell(x, y, self.grid[y][x], self.wall_colors[0])

    def refresh(self) -> None:
        self.path_animation_index = 0
        self.maze_animation_index = 0
        self.pattern_animation_index = 0
        self.position = self.entry
        self.mlx_maze.mlx_loop_hook(self.mlx_ptr, None, None)
        self.mlx_maze.mlx_clear_window(self.mlx_ptr, self.win_ptr)
        self.draw_maze()
        if self.is_touch_p:
            self.draw_path()

    def animate_path(self, _) -> None:
        if self.path_animation_index >= len(self.result) - 1:
            return
        x, y = self.result[self.path_animation_index]
        if (x, y) not in [self.entry, self.exit_]:
            self.draw_rectangle(
                x * self.cell_size, y * self.cell_size,
                self.cell_size, self.cell_size,
                0XFF22C55E
                )
            self.draw_cell(x, y, self.grid[y][x], self.wall_colors[0])
        self.path_animation_index += 1

    def animate_maze(self, _) -> None:
        if self.maze_animation_index < len(self.history):
            x, y = self.history[self.maze_animation_index]
            if (x, y) == self.entry:
                self.draw_entry()
            if (x, y) == self.exit_:
                self.draw_exit()
            self.draw_cell(x, y, self.grid[y][x], self.wall_colors[0])
            self.maze_animation_index += 1
        elif self.pattern_animation_index < len(self.pattern_42):
            x, y = self.pattern_42[self.pattern_animation_index]
            px = x * self.cell_size
            py = y * self.cell_size
            self.draw_rectangle(
                px, py, self.cell_size, self.cell_size, 0XFFFF0099
                )
            self.pattern_animation_index += 1
        return

    def key_hook(self, keycode: int, _) -> None:
        if keycode == 65307:
            self.mlx_maze.mlx_loop_exit(self.mlx_ptr)
            return

        if keycode in [ord('p'), ord('P')]:
            if not self.is_touch_p:
                self.refresh()
                self.mlx_maze.mlx_loop_hook(
                    self.mlx_ptr, self.animate_path, None
                    )
                self.is_touch_p = True
            else:
                self.is_touch_p = False
                self.refresh()

        if keycode == 65361:
            x, y = self.position
            if self.grid[y][x] & 8 == 8:
                return
            nx, ny = x - 1, y
            self.position = nx, ny
            if (nx, ny) == self.exit_:
                self.is_touch_p = False
                self.refresh()
                self.mlx_maze.mlx_loop_hook(
                    self.mlx_ptr, self.animate_path, None
                    )
                self.is_touch_p = True
                return
            px, py = nx * self.cell_size, ny * self.cell_size
            self.draw_rectangle(
                px, py, self.cell_size, self.cell_size, 0X8822C55E
                )
            self.draw_cell(nx, ny, self.grid[ny][nx], self.wall_colors[0])

        if keycode == 65362:
            x, y = self.position
            if self.grid[y][x] & 1 == 1:
                return
            nx, ny = x, y - 1
            self.position = nx, ny
            if (nx, ny) == self.exit_:
                self.is_touch_p = False
                self.refresh()
                self.mlx_maze.mlx_loop_hook(
                    self.mlx_ptr, self.animate_path, None
                    )
                self.is_touch_p = True
                return
            px, py = nx * self.cell_size, ny * self.cell_size
            self.draw_rectangle(
                px, py, self.cell_size, self.cell_size, 0X8822C55E
                )
            self.draw_cell(nx, ny, self.grid[ny][nx], self.wall_colors[0])

        if keycode == 65363:
            x, y = self.position
            if self.grid[y][x] & 2 == 2:
                return
            nx, ny = x + 1, y
            self.position = nx, ny
            if (nx, ny) == self.exit_:
                self.is_touch_p = False
                self.refresh()
                self.mlx_maze.mlx_loop_hook(
                    self.mlx_ptr, self.animate_path, None
                    )
                self.is_touch_p = True
                return
            px, py = nx * self.cell_size, ny * self.cell_size
            self.draw_rectangle(
                px, py, self.cell_size, self.cell_size, 0X8822C55E
                )
            self.draw_cell(nx, ny, self.grid[ny][nx], self.wall_colors[0])

        if keycode == 65364:
            x, y = self.position
            if self.grid[y][x] & 4 == 4:
                return
            nx, ny = x, y + 1
            self.position = nx, ny
            if (nx, ny) == self.exit_:
                self.is_touch_p = False
                self.refresh()
                self.mlx_maze.mlx_loop_hook(
                    self.mlx_ptr, self.animate_path, None
                    )
                self.is_touch_p = True
                return
            px, py = nx * self.cell_size, ny * self.cell_size
            self.draw_rectangle(
                px, py, self.cell_size, self.cell_size, 0X8822C55E
                )
            self.draw_cell(nx, ny, self.grid[ny][nx], self.wall_colors[0])

        if keycode == ord(' '):
            self.refresh()

        if keycode in [ord('c'), ord('C')]:
            self.wall_colors = self.wall_colors[1:] + self.wall_colors[:1]
            self.refresh()

    def run_maze(self) -> None:
        self.mlx_maze.mlx_loop_hook(self.mlx_ptr, self.animate_maze, None)
        self.mlx_maze.mlx_key_hook(self.win_ptr, self.key_hook, None)
        self.mlx_maze.mlx_loop(self.mlx_ptr)
