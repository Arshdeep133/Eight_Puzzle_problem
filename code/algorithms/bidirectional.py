from collections import deque
import time

def bidirectional_search(start_state):
    """
    Solves the 8-puzzle using Bidirectional Search.

    Args:
        start_state (list): The initial puzzle state as a 2D list.

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

    def state_to_tuple(state):
        return tuple(tuple(row) for row in state)

    def reconstruct_path(frontier_path, reverse_path):
        """Reconstructs the solution path from the two meeting points."""
        meeting_state = frontier_path[-1]
        reverse_path = list(reversed(reverse_path))
        return frontier_path + reverse_path[1:]

    # Bidirectional Search setup
    start_tuple = state_to_tuple(start_state)
    goal_state = [[(i * n + j + 1) % (n * n) for j in range(n)] for i in range(n)]
    goal_tuple = state_to_tuple(goal_state)
    start_time = time.time()
    base_timeout = 120  # Base timeout for 3x3 puzzles
    timeout = base_timeout * (n ** 2 / 9)  # Scale timeout proportionally to n^2
    if start_tuple == goal_tuple:
        return [start_state]

    # Queues for forward and backward search
    forward_queue = deque([(start_tuple, [start_state])])
    backward_queue = deque([(goal_tuple, [goal_state])])

    # Visited sets for forward and backward search
    forward_visited = {start_tuple: [start_state]}
    backward_visited = {goal_tuple: [goal_state]}

    while forward_queue and backward_queue:
        # Expand forward search
        if time.time() - start_time > timeout:
            print("Greedy terminated due to timeout.")
            return None
        current_forward, path_forward = forward_queue.popleft()
        for neighbor in get_neighbors([list(row) for row in current_forward]):
            neighbor_tuple = state_to_tuple(neighbor)
            if neighbor_tuple in backward_visited:
                return reconstruct_path(path_forward + [neighbor], backward_visited[neighbor_tuple])
            if neighbor_tuple not in forward_visited:
                forward_visited[neighbor_tuple] = path_forward + [neighbor]
                forward_queue.append((neighbor_tuple, path_forward + [neighbor]))

        # Expand backward search
        current_backward, path_backward = backward_queue.popleft()
        for neighbor in get_neighbors([list(row) for row in current_backward]):
            neighbor_tuple = state_to_tuple(neighbor)
            if neighbor_tuple in forward_visited:
                return reconstruct_path(forward_visited[neighbor_tuple], path_backward + [neighbor])
            if neighbor_tuple not in backward_visited:
                backward_visited[neighbor_tuple] = path_backward + [neighbor]
                backward_queue.append((neighbor_tuple, path_backward + [neighbor]))

    return None  # No solution found
