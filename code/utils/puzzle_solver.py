
def puzzle_reader(file_path):
    """Reads a single puzzle from a text file.

    Args:
        file_path (str): The path to the puzzle file.

    Returns:
        list: A 2D list representing the puzzle grid.
    """
    puzzle = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip():  # Ignore empty lines
                row = list(map(int, line.split()))
                puzzle.append(row)
    return puzzle

def solve_puzzle(puzzle, algorithm, ALGORITHMS, heuristic=None, pdbs=None):
    """Solves the puzzle using the specified algorithm.

    Args:
        puzzle (list): A 2D list representing the puzzle grid.
        algorithm (str): The name of the algorithm to use.

    Returns:
        list: A list of puzzle states showing the solution path.
    """

    if algorithm not in ALGORITHMS:
        raise ValueError(f"Unsupported algorithm: {algorithm}")
    if algorithm in ["a_star", "greedy", "ida_star"]:
        if heuristic is None:
            raise ValueError(f"Heuristic is required for {algorithm} algorithm.")
        return ALGORITHMS[algorithm](puzzle, heuristic, pdbs)
    return ALGORITHMS[algorithm](puzzle)

