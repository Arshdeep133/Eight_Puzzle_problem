from queue import PriorityQueue
import algorithms.heuristics
import time

def a_star(start_state, heuristic, pdbs = None):
    """Solves the puzzle using A* with the specified heuristic.

    Args:
        start_state (list): The initial puzzle state as a 2D list.
        heuristic (str): The heuristic to use ("manhattan" or "misplaced").

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
    elif heuristic == "inconsistent":
        heuristic_fn = algorithms.heuristics.inconsistent_heuristic
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

    # A* search
    start_time = time.time()
    base_timeout = 120  # Base timeout for 3x3 puzzles
    timeout = base_timeout * (n ** 2 / 9)  # Scale timeout proportionally to n^2
    start_state_tuple = tuple(tuple(row) for row in start_state)
    open_list = PriorityQueue()
    open_list.put((0 + heuristic_fn(start_state, n), 0, start_state, []))  # f = g + h
    closed_set = set()
    visited = {start_state_tuple: 0}

    while not open_list.empty():
        _, g, current_state, path = open_list.get()
        if time.time() - start_time > timeout:
            print("A* terminated due to timeout.")
            return None
        if is_goal(current_state):
            return path + [current_state]

        closed_set.add(tuple(tuple(row) for row in current_state))

        for neighbor in get_neighbors(current_state):
            neighbor_tuple = tuple(tuple(row) for row in neighbor)
            new_g = g + 1
            if neighbor_tuple not in visited or visited[neighbor_tuple] > new_g:
                visited[neighbor_tuple] = new_g
                f = new_g + heuristic_fn(neighbor, n)
                open_list.put((f, new_g, neighbor, path + [current_state]))

    return None  # No solution found
