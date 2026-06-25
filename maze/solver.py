def bfs(
		entry: tuple[int, int],
		exit_: tuple[int, int],
		grid: list[list[int]],
		width: int,
		height: int) -> list[tuple[int, int]]:
	xs, ys = exit_
	queue: list[tuple[int, int]] = []
	couple: list[tuple[tuple[int, int], tuple[int, int]]] = []
	queue.append(entry)
	visited: set[tuple[int, int]] = set([entry])
	is_break: bool = False
	while queue and not is_break:
		(xe, ye) = queue.pop(0)
		for dx, dy, direction in [(-1, 0, 8), (1, 0, 2), (0, -1, 1), (0, 1, 4)]:
			nx = xe + dx
			ny = ye + dy

			if not (0 <= nx < width and 0 <= ny < height):
				continue

			if (nx, ny) in visited:
				continue

			if (grid[ye][xe] & direction) == 0:
				queue.append((nx, ny))
				couple.append(((xe, ye), (nx, ny)))
				visited.add((nx, ny))

			if nx == xs and ny == ys:
				couple.append(((xe, ye), (nx, ny)))
				is_break = True
				break

	result:list[tuple[int, int]] = []
	pos1, pos2 = couple[len(couple) - 1]
	result.append(pos2)
	for c1, c2 in couple[-2::-1]:
		if c2 == pos1:
			result.append(c2)
			pos1 = c1
		if pos1 == entry:
			break
	result.append(entry)
	result.reverse()
	return result
