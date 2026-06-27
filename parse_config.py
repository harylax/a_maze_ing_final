import sys


class MazeConfigError(Exception):
    def __init__(self, message):
        super().__init__(message)


class MazeConfig:
    def __init__(self, filename: str) -> None:
        self.width: int = 20
        self.height: int = 15
        self.entry: tuple[int, int] = (0, 0)
        self.exit_: tuple[int, int] = (19, 14)
        self.output_file: str = 'maze.txt'
        self.perfect: bool = True
        self.seed: int = 42
        self.missing_config: list[str] = []
        self.read_file(filename)

    def read_file(self, filename: str) -> None:
        content: str | None = None

        try:
            with open(filename) as f:
                content = f.read().strip()
        except OSError as err:
            raise MazeConfigError(f"Config file error: {err}")
        if not content:
            raise MazeConfigError("Empty config file.")
        result: dict[str, str] = self.content_to_dict(content)
        if self.missing_config:
            print(
                f"{', '.join(error for error in self.missing_config)} "
                "are missing in the config file", file=sys.stderr
                )
            sys.exit(1)

        is_error: bool = False
        try:
            self.width = int(result['WIDTH'])
        except ValueError as err:
            print(f"WIDTH Value Error: {err}", file=sys.stderr)
            is_error = True
        try:
            self.height = int(result['HEIGHT'])
        except ValueError as err:
            print(f"HEIGHT Value Error: {err}", file=sys.stderr)
            is_error = True
        try:
            self.seed = int(result['SEED'])
        except ValueError as err:
            print(f"SEED Value Error: {err}", file=sys.stderr)
            is_error = True
        try:
            x, y = result['ENTRY'].split(',')
            self.entry = (int(x), int(y))
        except ValueError as err:
            print(f"Value Error of ENTRY coordinates: {err}", file=sys.stderr)
            is_error = True
        try:
            x, y = result['EXIT'].split(',')
            self.exit_ = (int(x), int(y))
        except ValueError as err:
            print(f"Value Error of EXIT coordinates: {err}", file=sys.stderr)
            is_error = True

        if result['PERFECT'].capitalize() == 'True':
            self.perfect = True
        elif result['PERFECT'].capitalize() == 'False':
            self.perfect = False
        else:
            print("PERFECT Value Error: Cast to boolean error", file=sys.stderr)
            is_error = True

        self.output_file = result['OUTPUT_FILE']

        if is_error:
            sys.exit(1)

        try:
            self.validate_config()
        except MazeConfigError as err:
            print(err)
            sys.exit(1)

    def content_to_dict(self, content: str) -> dict[str, str]:
        result: dict[str, str] = {}
        lines: list[str] = content.splitlines()
        for line in lines:
            if line.startswith('#'):
                continue

            if '=' not in line:
                print(
                    "The configuration file must contain one "
                    "'KEY=VALUE' pair per line.",
                    file=sys.stderr
                    )
                sys.exit(1)

            raw = line.split('=', 1)
            key: str = raw[0].strip().upper()
            value: str = raw[1].strip()

            if key in result:
                print(f"Got duplicate {key}")
                continue

            result[key] = value

        if 'WIDTH' not in result.keys():
            self.missing_config.append('WIDTH')
        if 'HEIGHT' not in result.keys():
            self.missing_config.append('HEIGHT')
        if 'ENTRY' not in result.keys():
            self.missing_config.append('ENTRY')
        if 'EXIT' not in result.keys():
            self.missing_config.append('EXIT')
        if 'OUTPUT_FILE' not in result.keys():
            self.missing_config.append('OUTPUT_FILE')
        if 'PERFECT' not in result.keys():
            self.missing_config.append('PERFECT')
        return result

    def validate_config(self) -> None:
        if self.width < 2:
            raise MazeConfigError("WIDTH should be a positive value and greater than.")
        if self.height < 2:
            raise MazeConfigError("WIDTH should be a positive value and greater than.")
        if not (0 <= self.entry[0] < self.width and 0 <= self.entry[1] < self.height):
            raise MazeConfigError("ENTRY coordinates should be in the grid.")
        if not (0 <= self.exit_[0] < self.width and 0 <= self.exit_[1] < self.height):
            raise MazeConfigError("EXIT coordinates should be in the grid.")

    def __str__(self) -> str:
        return (
            f"width={self.width}\n"
            f"height={self.height}\n"
            f"entry={self.entry}\n"
            f"exit_={self.exit_}\n"
            f"output_file='{self.output_file}'\n"
            f"perfect={self.perfect}\n"
            f"seed={self.seed}\n"
        )
