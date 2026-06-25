from parse_config import MazeConfig
from maze.generator import MazeGenerator
from mlx_maze import MlxMaze
import sys

def write_output(mazegen: MazeGenerator) -> None:
    try:
        with open('maze.txt', 'w') as f:
            result_maze_hexa: str = "\n".join("".join(format(cell, "X") for cell in row) for row in mazegen.grid)
            entry: str = f"{mazegen.entry[0]},{mazegen.entry[1]}"
            exit_: str = f"{mazegen.exit_[0]},{mazegen.exit_[1]}"
            result_path: str = f"{mazegen.result_path()}"
            output: str = f"{result_maze_hexa}\n\n" + f"{entry}\n" + f"{exit_}\n" + f"{result_path}" 
            f.write(output)
    except OSError as err:
        print(f"Error to write into the file maze.txt: {err}")

def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        return
    config: MazeConfig = MazeConfig(sys.argv[1])
    mazegen: MazeGenerator = MazeGenerator(
        config.width,
        config.height,
        config.entry,
        config.exit_,
        config.output_file,
        config.perfect,
        config.seed
        )
    mazegen.generate()
    write_output(mazegen)
    render: MlxMaze = MlxMaze(mazegen)
    render.run_maze()

main()