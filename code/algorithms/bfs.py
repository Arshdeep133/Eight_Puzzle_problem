from collections import deque
import time

def bfs(start_state):
    """Solves the puzzle using BFS.

    Args:
        start_state (list): The initial puzzle state.

    Returns:
        list: The solution path as a list of puzzle states.
    """

    n = len(start_state)

    def is_goal(state):
        goal = [[(i * n + j + 1) % (n * n) for j in range(n)] for i in range(n)]
        return state == goal

    def get_neighbors(state):
        neighbors = []
        # Find the blank (0) position
        blank_x, blank_y = next((x, y) for x in range(n) for y in range(n) if state[x][y] == 0)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        for dx, dy in directions:
            nx, ny = blank_x + dx, blank_y + dy
            if 0 <= nx < n and 0 <= ny < n:
                # Swap blank with the neighbor and create a new state
                new_state = [row[:] for row in state]
                new_state[blank_x][blank_y], new_state[nx][ny] = new_state[nx][ny], new_state[blank_x][blank_y]
                neighbors.append(new_state)
        return neighbors
    
    visited = set()
    queue = deque([(start_state, [])])  # (current state, path to current state)
    start_time = time.time()
    base_timeout = 120  # Base timeout for 3x3 puzzles
    timeout = base_timeout * (n ** 2 / 9)  # Scale timeout proportionally to n^2
    while queue:
        current_state, path = queue.popleft()
        if time.time() - start_time > timeout:
            print("BFS terminated due to timeout.")
            return None
        # Check if the current state is the goal state
        if is_goal(current_state):
            return path + [current_state]

        # Mark the current state as visited
        visited.add(tuple(map(tuple, current_state)))

        # Add all valid neighbors to the queue
        for neighbor in get_neighbors(current_state):
            if tuple(map(tuple, neighbor)) not in visited:
                queue.append((neighbor, path + [current_state]))

    return None  # If no solution exists