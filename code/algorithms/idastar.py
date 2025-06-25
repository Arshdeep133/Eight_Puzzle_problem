import algorithms.heuristics
import time

def ida_star(start_state, heuristic, pdbs=None):
    """Solves the puzzle using IDA* with the specified heuristic.

    Args:
        start_state (list): The initial puzzle state as a 2D list.
        heuristic (str): The heuristic to use ("manhattan", "misplaced", etc.).
        pdbs (dict): Pattern databases for specific heuristics, if needed.

    Returns:
        list: The solution path as a list of puzzle states.
    """

    n = len(start_state)

    def is_goal(state):
        goal = [[(i * n + j + 1) % (n * n) for j in range(n)] for i in range(n)]
        return state == goal

    def get_neighbors(state):
        neighbors = []
        blank_x, blank_y = next((x, y) for x in range(n) for y in range(n) if state[x][y] == 0)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        for dx, dy in directions:
            nx, ny = blank_x + dx, blank_y + dy
            if 0 <= nx < n and 0 <= ny < n:
                new_state = [row[:] for row in state]
                new_state[blank_x][blank_y], new_state[nx][ny] = new_state[nx][ny], new_state[blank_x][blank_y]
                neighbors.append(new_state)
        return neighbors

    # Choose heuristic
    if heuristic == "manhattan":
        heuristic_fn = algorithms.heuristics.manhattan_distance
    elif heuristic == "misplaced":
        heuristic_fn = algorithms.heuristics.misplaced_tiles
    elif heuristic == "linear_conflict":
        heuristic_fn = algorithms.heuristics.linear_conflict
    elif heuristic == "non_additive_pdb":
        if pdbs is None:
            raise ValueError("Pattern databases (pdbs) must be provided for non_additive_pdb heuristic.")
        heuristic_fn = lambda state, n: algorithms.heuristics.non_additive_pdb(state, n, pdbs)
    elif heuristic == "symmetry":
        heuristic_fn = lambda state, n: algorithms.heuristics.symmetry_heuristic(state, n, algorithms.heuristics.manhattan_distance)
    elif heuristic == "dual_lookup":
        if pdbs is None or "forward" not in pdbs or "backward" not in pdbs:
            raise ValueError("Pattern databases (pdbs) for dual lookup must include 'forward' and 'backward'.")
        heuristic_fn = lambda state, n: algorithms.heuristics.dual_lookup_heuristic(state, n, pdbs["forward"], pdbs["backward"])
    elif heuristic == "disjointpdb":
        heuristic_fn = algorithms.heuristics.disjointpdb
    else:
        raise ValueError(f"Unknown heuristic: {heuristic}")

    def search(state, g, threshold, path):
        """Recursive DFS-based search with pruning."""
        f = g + heuristic_fn(state, n)
        if f > threshold:
            return f, None
        if is_goal(state):
            return f, path + [state]

        min_threshold = float('inf')
        for neighbor in get_neighbors(state):
            if neighbor not in path:  # Avoid cycles
                new_g = g + 1
                t, result = search(neighbor, new_g, threshold, path + [state])
                if result is not None:
                    return t, result
                min_threshold = min(min_threshold, t)

        return min_threshold, None

    # IDA* search
    start_time = time.time()
    base_timeout = 120  # Base timeout for 3x3 puzzles
    timeout = base_timeout * (n ** 2 / 9)  # Scale timeout proportionally to n^2
    threshold = heuristic_fn(start_state, n)

    while True:
        if time.time() - start_time > timeout:
            print("IDA* terminated due to timeout.")
            return None
        t, result = search(start_state, 0, threshold, [])
        if result is not None:
            return result
        if t == float('inf'):  # No solution
            return None
        threshold = t
