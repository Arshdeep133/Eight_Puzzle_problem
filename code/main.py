import sys
import time as timer

# Import utilities
from utils.puzzle_solver import puzzle_reader, solve_puzzle
from utils.visualization import visualize_puzzle_solution
from utils.puzzle_generator import generate_puzzle
from utils.comparison import compare_algorithms

# Import algorithms
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.astar import a_star
from algorithms.iddfs import iddfs
from algorithms.greedy import greedy
from algorithms.idastar import ida_star
from algorithms.reverse_bfs import reverse_bfs
from algorithms.bidirectional import bidirectional_search
from algorithms.heuristics import generate_pdb, generate_dual_pdbs

# Dictionary of supported algorithms
ALGORITHMS = {
    "bfs": bfs,
    "dfs": dfs,
    "a_star": a_star,
    "bidirectional": bidirectional_search,
    "iddfs": iddfs,
    "greedy": greedy,
    "ida_star": ida_star,
    "reverse_bfs": reverse_bfs
}

# List of supported heuristics
HEURISTICS = [
    "manhattan", "misplaced", "linear_conflict", "inconsistent",
    "non_additive_pdb", "symmetry", "dual_lookup", "disjointpdb"
]

def determine_puzzle_size(puzzle):
    """Determine the size of the puzzle dynamically."""
    return len(puzzle)

def solve_and_visualize(puzzle, algorithm, heuristic=None, pdbs=None):
    """Solve the puzzle using the selected algorithm and visualize the solution."""
    start_time = timer.time()
    solution_path = solve_puzzle(puzzle, algorithm, ALGORITHMS, heuristic, pdbs)
    elapsed_time = timer.time() - start_time

    if solution_path:
        print(f"\nNumber of Steps: {len(solution_path) - 1}")
        print(f"CPU Time: {elapsed_time:.3f} seconds")
        visualize_puzzle_solution(solution_path)
    else:
        print(f"No solution found for {algorithm.upper()}.")

def prepare_puzzle_and_pdb(input_arg, algorithm, heuristic):
    """Prepare the puzzle and pattern databases if needed."""
    try:
        # Load puzzle from file or generate it
        if input_arg.endswith(".txt"):
            puzzle = puzzle_reader(input_arg)
        elif input_arg.isdigit() and int(input_arg) >= 3:
            puzzle = puzzle_reader(generate_puzzle(int(input_arg), 1))
        else:
            raise ValueError("Invalid input. Provide a valid file path or a number >= 3.")

        # Generate pattern databases if required
        n = determine_puzzle_size(puzzle)
        pdbs = None
        if heuristic == "non_additive_pdb":
            pdbs = generate_pdb(puzzle, n)
        elif heuristic == "dual_lookup":
            print("Generating pattern databases for dual lookup...")
            goal_state = [[(i * n + j + 1) % (n * n) for j in range(n)] for i in range(n)]
            pdbs = generate_dual_pdbs(puzzle, goal_state, [1, 2, 3, 4])

        return puzzle, pdbs

    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        sys.exit(1)

def print_solution_header(algorithm, heuristic=None):
    """Print the header for the solution visualization."""
    if heuristic:
        print(f"\nVisualizing solution for {algorithm.upper()} ({heuristic.upper()}) algorithm:")
    else:
        print(f"\nVisualizing solution for {algorithm.upper()} algorithm:")

def compare_algorithms_and_display_results(puzzle):
    """Compare all algorithms on the given puzzle and display results."""
    results = compare_algorithms(puzzle)
    print("\nComparison Results:")
    for algorithm, metrics in results.items():
        print(f"\n{algorithm.upper()}:")
        for metric, value in metrics.items():
            print(f"  {metric}: {value}")

def main():
    """Main function to handle arguments, solve puzzles, and visualize results."""
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: python main.py <file_to_solve|size> <algorithm_to_use> [<heuristic>]")
        sys.exit(1)

    # Parse arguments
    input_arg = sys.argv[1]
    algorithm = sys.argv[2].lower()
    heuristic = sys.argv[3].lower() if len(sys.argv) == 4 else None

    # Validate the algorithm
    if algorithm not in ALGORITHMS and algorithm != "all":
        print(f"Unsupported algorithm: {algorithm}. Available algorithms: {', '.join(ALGORITHMS.keys())}, all.")
        sys.exit(1)

    # Validate the heuristic
    if algorithm in ["a_star", "greedy", "ida_star"] and heuristic not in HEURISTICS:
        print(f"Available heuristics for {algorithm.upper()}: {', '.join(HEURISTICS)}.")
        sys.exit(1)

    # Prepare the puzzle and pattern databases
    puzzle, pdbs = prepare_puzzle_and_pdb(input_arg, algorithm, heuristic)

    # Solve the puzzle
    if algorithm == "all":
        compare_algorithms_and_display_results(puzzle)
    else:
        print_solution_header(algorithm, heuristic)
        solve_and_visualize(puzzle, algorithm, heuristic, pdbs)

if __name__ == "__main__":
    main()
