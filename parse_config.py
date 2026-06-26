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
        self.filename: str = filename
        self.errors_list: list[str] = []
        self.read_file()

    def read_file(self) -> None:
        content: str | None = None
        try:
            with open(self.filename) as f:
                content = f.read().strip()
        except OSError as err:
            raise MazeConfigError(f"Config file error: {err}")
        result: dict[str, str] = self.content_to_dict(content)
        if self.errors_list:
            for error in self.errors_list:
                print(f"{error} missing in the config file")
            exit(1)
        try:
            self.width = int(result['WIDTH'])
            self.height = int(result['HEIGHT'])
            self.seed = int(result['SEED'])
            x, y = result['ENTRY'].split(',')
            self.entry = (int(x), int(y))
            x, y = result['EXIT'].split(',')
            self.exit_ = (int(x), int(y))
            self.output_file = result['OUTPUT_FILE']
            if result['PERFECT'].strip().capitalize() == 'True':
                self.perfect = True
            elif result['PERFECT'].strip().capitalize() == 'False':
                self.perfect = False
            else:
                raise MazeConfigError("Casting to boolean error")
        except ValueError as err:
            print(f"Value error: {err}")
        try:
            self.validate_config()
        except MazeConfigError as err:
            print(err)
            exit(1)

    def content_to_dict(self, content: str) -> dict[str, str]:
        result: dict[str, str] = {}
        lines: list[str] = content.splitlines()
        for line in lines:
            if line.startswith('#'):
                continue
            raw = line.split('=', 1)
            result[raw[0].strip().upper()] = raw[1].strip()
        if 'WIDTH' not in result.keys():
            self.errors_list.append('WIDTH')
        if 'HEIGHT' not in result.keys():
            self.errors_list.append('HEIGHT')
        if 'ENTRY' not in result.keys():
            self.errors_list.append('ENTRY')
        if 'EXIT' not in result.keys():
            self.errors_list.append('EXIT')
        if 'OUTPUT_FILE' not in result.keys():
            self.errors_list.append('OUTPUT_FILE')
        if 'PERFECT' not in result.keys():
            self.errors_list.append('PERFECT')
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
            f"filename='{self.filename}'\n"
        )
