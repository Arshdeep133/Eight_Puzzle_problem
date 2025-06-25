from collections import deque
import time

def iddfs(start_state):
    """Solves the puzzle using IDS.

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

    def dls(start_state, depth):
        stack = [(start_state, [])]  
        while stack:
            current_state, path = stack.pop()
            if time.time() - start_time > timeout:
                print("iddfs terminated due to timeout.")
                return None
            if is_goal(current_state):
                return path + [current_state]
            if len(path) == depth:
                continue
            for neighbor in get_neighbors(current_state):
                stack.append((neighbor, path + [current_state]))
        return None
            
    start_time = time.time()
    base_timeout = 120  # Base timeout for 3x3 puzzles
    timeout = base_timeout * (n ** 2 / 9)  # Scale timeout proportionally to n^2

    for x in range(0, 100000):
        result = dls(start_state, x)
        if result is not None:
            return result

    return None  