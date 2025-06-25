from collections import deque

def reverse_bfs(start_state):
    """
    Solves the puzzle using Reverse BFS.

    Args:
        start_state (list): The initial puzzle state as a 2D list.

    Returns:
        list: The solution path as a list of puzzle states.
    """
    n = len(start_state)  # Calculate puzzle size internally

    def is_goal(state):
        """Checks if the current state is the goal state."""
        goal = [[(i * n + j + 1) % (n * n) for j in range(n)] for i in range(n)]
        return state == goal

    def get_neighbors(state):
        """Generates all valid neighboring states by moving the blank space."""
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

    # Initialize Reverse BFS
    goal_state = [[(i * n + j + 1) % (n * n) for j in range(n)] for i in range(n)]
    goal_tuple = tuple(tuple(row) for row in goal_state)
    visited = set()
    queue = deque([(goal_state, [])])  # Each element is (current_state, path_to_current_state)

    while queue:
        current_state, path = queue.popleft()
        state_tuple = tuple(tuple(row) for row in current_state)

        if state_tuple in visited:
            continue

        visited.add(state_tuple)

        if current_state == start_state:
            return path + [current_state]

        for neighbor in get_neighbors(current_state):
            neighbor_tuple = tuple(tuple(row) for row in neighbor)
            if neighbor_tuple not in visited:
                queue.append((neighbor, path + [current_state]))

    return None  # No solution found
