from collections import deque
from heapq import heappush, heappop
from itertools import permutations
from multiprocessing import Pool
import algorithms.pdb_creation as temp
import numpy as np


def manhattan_distance(state, n):
    """Calculates the total Manhattan distance of the puzzle state."""
    distance = 0
    for x in range(n):
        for y in range(n):
            value = state[x][y]
            if value != 0:
                target_x = (value - 1) // n
                target_y = (value - 1) % n
                distance += abs(x - target_x) + abs(y - target_y)
    return distance

def misplaced_tiles(state, n):
    """Calculates the number of misplaced tiles."""
    count = 0
    goal = [[(i * n + j + 1) % (n * n) for j in range(n)] for i in range(n)]
    for x in range(n):
        for y in range(n):
                if state[x][y] != goal[x][y]:
                    count += 1
    return count

def linear_conflict(state, n):
    """Manhattan distance + penalty for linear conflicts."""
    conflict_count = 0
    manhattan = manhattan_distance(state, n)

    # Check each row and column for conflicts
    for row in range(n):
        for col in range(n):
            value = state[row][col]
            if value == 0:
                continue
            target_row, target_col = (value - 1) // n, (value - 1) % n

            # Linear conflict in the same row
            if target_row == row:
                for next_col in range(col + 1, n):
                    next_value = state[row][next_col]
                    if next_value != 0 and (next_value - 1) // n == row and next_value < value:
                        conflict_count += 2  # Penalize linear conflict

            # Linear conflict in the same column
            if target_col == col:
                for next_row in range(row + 1, n):
                    next_value = state[next_row][col]
                    if next_value != 0 and (next_value - 1) % n == col and next_value < value:
                        conflict_count += 2  # Penalize linear conflict

    return manhattan + conflict_count

def inconsistent_heuristic(state, n):
    """Inconsistent heuristic: Double the Manhattan distance for tiles with even numbers."""
    distance = 0
    for x in range(n):
        for y in range(n):
            value = state[x][y]
            if value != 0:
                target_x = (value - 1) // n
                target_y = (value - 1) % n
                penalty = 2 if value % 2 == 0 else 1
                distance += penalty * (abs(x - target_x) + abs(y - target_y))
    return distance

def generate_goal_state(n):
    if isinstance(n, list):  # Check if n is a list
        n = len(n)  # Convert list to its size
    return [[(i * n + j + 1) % (n * n) for j in range(n)] for i in range(n)]

def is_solvable(puzzle, n):
    """Checks if a given puzzle state is solvable."""
    flat = [tile for row in puzzle for tile in row if tile != 0]
    inversions = sum(
        1 for i in range(len(flat)) for j in range(i + 1, len(flat)) if flat[i] > flat[j]
    )
    return inversions % 2 == 0

def validate_puzzle_input(puzzle, n):
    """Validates that the puzzle is a proper n x n 2D list."""
    if not isinstance(puzzle, list) or len(puzzle) != n:
        raise ValueError(f"Invalid puzzle size: {len(puzzle)}. Expected {n} rows.")
    
    for row in puzzle:
        if not isinstance(row, list) or len(row) != n:
            raise ValueError(f"Row size mismatch. Expected {n} elements, but got {len(row)}.")
        if not all(isinstance(tile, int) for tile in row):
            raise ValueError("Puzzle contains non-integer values.")
    
    # Check for valid tiles (must be the numbers from 0 to n*n-1)
    tiles = [tile for row in puzzle for tile in row]
    if set(tiles) != set(range(n * n)):
        raise ValueError(f"Invalid puzzle tiles. Expected: {set(range(n * n))}, Found: {set(tiles)}")

def generate_pdb(puzzle, n):
    """
    Generates a Non-Additive Pattern Database (PDB) for the puzzle.
    The PDB stores the minimum number of moves required to solve the subproblem for specific tile patterns.

    Args:
        puzzle (list): The current state of the puzzle.
        n (int): The size of the puzzle (n x n).

    Returns:
        dict: A dictionary where the keys are tile patterns (tuples) and the values are their corresponding distances.
    """
    print("Generating PDB")
    #if not is_solvable(puzzle, n):
        #raise ValueError("The given puzzle state is unsolvable.")

    goal_state = generate_goal_state(n)
    flat_puzzle = [tile for row in puzzle for tile in row]
    flat_goal = [tile for row in goal_state for tile in row]
    misplaced_tiles_list = [
        flat_puzzle[i]
        for i in range(n * n)
        if flat_puzzle[i] != flat_goal[i] and flat_puzzle[i] != 0
    ]

     # Ensure that all tiles are considered in the pattern
    if len(misplaced_tiles_list) < n * n:
        # Fill in the remaining missing tiles (the ones that are correctly placed)
        for tile in range(n * n):
            if tile not in misplaced_tiles_list:
                misplaced_tiles_list.append(tile)

    patterns = [tuple(sorted(misplaced_tiles_list))]
    validate_puzzle_input(puzzle, n)
    print(f"Generated patterns: {patterns}")
    with Pool() as pool:
        pdb_values = pool.starmap(calculate_pdb_value, [(pattern, n) for pattern in patterns])

    return {pattern: value for pattern, value in zip(patterns, pdb_values)}


def calculate_pdb_value(pattern, n):
    """Calculates the minimum moves required to solve the given pattern."""
    goal_state = list(range(1, n * n)) + [0]
    start_state = list(pattern)
    print(start_state)
    print(goal_state)
    if len(start_state) != n * n:
        raise ValueError(f"State size {len(start_state)} does not match expected {n * n}.")
    start_state_2d = [start_state[i * n:(i + 1) * n] for i in range(n)]
    queue = []
    heappush(queue, (linear_conflict(start_state_2d, n), 0, start_state))
    visited = set()
    visited.add(tuple(start_state))

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        _, depth, state = heappop(queue)
        if state == goal_state:
            return depth

        zero_idx = state.index(0)
        zero_row, zero_col = zero_idx // n, zero_idx % n

        for dr, dc in directions:
            new_row, new_col = zero_row + dr, zero_col + dc
            if 0 <= new_row < n and 0 <= new_col < n:
                new_idx = new_row * n + new_col
                new_state = list(state)
                new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]

                if tuple(new_state) not in visited:
                    visited.add(tuple(new_state))
                    new_state_2d = [new_state[i * n:(i + 1) * n] for i in range(n)]
                    heappush(queue, (depth + 1 + linear_conflict(new_state_2d, n), depth + 1, new_state))

    return float('inf')

def non_additive_pdb(state, n, pdb):
    """
    Non-additive Pattern Database (PDB) heuristic for the puzzle state.
    Instead of summing the PDB values, we combine them using a non-additive strategy (max in this case).
    
    Args:
        state (list): The current puzzle state.
        n (int): The size of the puzzle (n x n).
        pdb (dict): The pattern database to use for the heuristic.
    
    Returns:
        int: The non-additive heuristic value for the current state.
    """
    distance = 0
    for x in range(n):
        for y in range(n):
            value = state[x][y]
            if value != 0:  
                pattern = tuple(sorted([state[x][y] for x in range(n) for y in range(n) if state[x][y] != 0]))  # Example pattern
                if pattern in pdb:
                    distance = max(distance, pdb[pattern])
    
    return distance

def symmetry_heuristic(state, n, heuristic_function):
    """
    Calculates a heuristic value using symmetric states of the puzzle.

    Args:
        state (list): The current puzzle state.
        n (int): The size of the puzzle (n x n).
        heuristic_function (function): A heuristic function (e.g., Manhattan distance).

    Returns:
        int: The heuristic value considering all symmetric states.
    """
    state_array = np.array(state)
    transformations = [
        state_array,  # Original
        np.flip(state_array, axis=0),  # Vertical flip
        np.flip(state_array, axis=1),  # Horizontal flip
        np.rot90(state_array, k=1),  # 90-degree rotation
        np.rot90(state_array, k=2),  # 180-degree rotation
        np.rot90(state_array, k=3),  # 270-degree rotation
    ]

    heuristic_values = [
        heuristic_function(trans.tolist(), n)
        for trans in transformations
    ]

    return min(heuristic_values)  # Use the minimum heuristic among symmetric states

def dual_lookup_heuristic(state, n, pdb_forward, pdb_backward):
    """
    Calculates a heuristic using dual lookup with forward and backward pattern databases.

    Args:
        state (list): The current puzzle state.
        n (int): The size of the puzzle (n x n).
        pdb_forward (dict): Forward pattern database.
        pdb_backward (dict): Backward pattern database.

    Returns:
        int: The combined heuristic value.
    """
    state_tuple = tuple(tuple(row) for row in state)  # Convert to hashable type
    h_forward = pdb_forward.get(state_tuple, float('inf'))
    h_backward = pdb_backward.get(state_tuple, float('inf'))
    return max(h_forward, h_backward)  # Combine using max or another strategy

def generate_dual_pdbs(start_state, goal_state, pattern):
    """
    Generates forward and backward pattern databases for dual lookup.

    Args:
        start_state (list): The starting state of the puzzle as a 2D list.
        goal_state (list): The goal state of the puzzle as a 2D list.
        pattern (list): A list of tiles to include in the pattern.

    Returns:
        dict: A dictionary containing forward and backward PDBs.
    """
    def generate_pdb_internal(reference_state):
        """
        Generates a Pattern Database (PDB) for the given reference state.

        Args:
            reference_state (list): The reference state for which the PDB is generated.

        Returns:
            dict: A dictionary where keys are tuple representations of puzzle states
                  and values are the minimum cost to reach the reference state.
        """
        n = len(reference_state)
        reference_tuple = tuple(tuple(row) for row in reference_state)

        # Initialize PDB with the reference state
        pdb = {reference_tuple: 0}
        queue = deque([reference_state])

        while queue:
            current_state = queue.popleft()
            current_tuple = tuple(tuple(row) for row in current_state)
            current_cost = pdb[current_tuple]

            # Generate neighbors by moving the blank tile
            blank_x, blank_y = next((x, y) for x in range(n) for y in range(n) if current_state[x][y] == 0)
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
            for dx, dy in directions:
                nx, ny = blank_x + dx, blank_y + dy
                if 0 <= nx < n and 0 <= ny < n:
                    # Create new state
                    neighbor_state = [row[:] for row in current_state]
                    neighbor_state[blank_x][blank_y], neighbor_state[nx][ny] = neighbor_state[nx][ny], neighbor_state[blank_x][blank_y]
                    neighbor_tuple = tuple(tuple(row) for row in neighbor_state)

                    # Only store states where the pattern matches
                    if neighbor_tuple not in pdb and all(tile in pattern or tile == 0 for row in neighbor_state for tile in row):
                        pdb[neighbor_tuple] = current_cost + 1
                        queue.append(neighbor_state)

        return pdb

    # Generate forward and backward PDBs
    pdb_forward = generate_pdb_internal(goal_state)   # Forward PDB: Goal as reference
    pdb_backward = generate_pdb_internal(start_state) # Backward PDB: Start as reference
    return {"forward": pdb_forward, "backward": pdb_backward}


def disjointpdb(state, n):
    # temp.create_disjoint_pdb(n)
    
    ### for n = 3 
    if n == 3:
        ## 3 - 3 - 2 disjoint set
        pdb_cost = temp.load_pdb("disjoint_pdb3.txt")
        groups = disjoint_state(state, n)

        ## 4 - 4 disjoint set
        # pdb_cost = temp.load_pdb("disjoint_pdb3_1.txt")
        # groups = disjoint_state2(state, n)

    ### for n = 4
    elif n == 4:
        ## 4 - 4 - 4 - 3  disjoint set
        #pdb_cost = temp.load_pdb("disjoint_pdb4.txt")
        #groups = disjoint_state(state, n)
        
        ## 8 - 7 disjoint set
        #pdb_cost = temp.load_pdb("disjoint_pdb4_1.txt")
        #groups = disjoint_state3(state, n)
        pass


    pdb_dict = dict(pdb_cost)
    heuristic = 0
    for group in groups:
        group_tuple = tuple(group)
        heuristic += pdb_dict.get(group_tuple, float('inf'))
    return heuristic


def disjoint_state(state, n):
    ## n - n - n-1 disjoint set
    size = n * n 
    groups = []
    flattened_state = temp.flatten_2d_array(state)
    for group_index in range(n):
        start_val = group_index * n + 1
        end_val = (group_index + 1) * n

        group = [tile if start_val <= tile <= end_val else -1 for tile in flattened_state]
        groups.append(group)

    return groups

def disjoint_state2(state, n):
    ## 4 - 4 disjoint set
    flattened_state = temp.flatten_2d_array(state)
    set_1 = [1, 2, 4, 5]
    set_2 = [3, 6, 7, 8]
    groups = [[-1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1]]
    for i in range(n*n):
        if flattened_state[i] != 0:
            if flattened_state[i] in set_1:
                groups[0][i] = flattened_state[i]
            elif flattened_state[i] in set_2:
                groups[1][i] = flattened_state[i]
    return groups
