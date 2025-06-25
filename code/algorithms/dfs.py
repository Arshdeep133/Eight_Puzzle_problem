import time

def flatten(state):
    """Flattens a 2D list into a 1D list."""
    return [elem for row in state for elem in row]

def dfs(start_state):
    """Solves the puzzle using DFS.

    Args:
        start_state (list): The initial puzzle state as a flattened list.

    Returns:
        list: The solution path as a list of puzzle states.
    """
    n = len(start_state)

    def is_goal(state):
        goal = [[(i * n + j + 1) % (n * n) for j in range(n)] for i in range(n)]
        return state == goal

    def get_neighbors(state):
        neighbors = []
        blank_index = state.index(0)
        blank_x, blank_y = divmod(blank_index, n)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        for dx, dy in directions:
            nx, ny = blank_x + dx, blank_y + dy
            if 0 <= nx < n and 0 <= ny < n:
                new_blank_index = nx * n + ny
                new_state = state[:]
                new_state[blank_index], new_state[new_blank_index] = new_state[new_blank_index], new_state[blank_index]
                neighbors.append(new_state)
        return neighbors
    start_state_flat = flatten(start_state)

    if 0 not in start_state_flat:
        print("Error: The start state must contain a blank tile (0).")
        return None
    start_time = time.time()
    base_timeout = 120  # Base timeout for 3x3 puzzles
    timeout = base_timeout * (n ** 2 / 9)  # Scale timeout proportionally to n^2
    visited = []
    stack = [(start_state_flat, [])]  

    while stack:
        if time.time() - start_time > timeout:
            print("DFS terminated due to timeout.")
            return None
        current_state, path = stack.pop()

        if is_goal(current_state):
            return path + [current_state]

        visited.append(current_state)  

        for neighbor in get_neighbors(current_state):
            if neighbor not in visited:  
                stack.append((neighbor, path + [current_state]))

    return None  