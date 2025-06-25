import os
from utils.puzzle_solver import puzzle_reader
from utils.puzzle_generator import generate_puzzle
from utils.comparison import compare_all_puzzle, generate_dynamic_graphs


def create_output_directory(output_dir):
    """Create output directory if it doesn't exist."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


def run_incremental_comparisons(size, output_dir):
    """
    Run puzzle generation and comparison incrementally for a given puzzle size.

    Args:
        size (int): The size of the puzzles (e.g., 3x3, 4x4).
        output_dir (str): Directory to save summary results and graphs.
    """
    for num_puzzles in range(1, 6):  # From 1 to 5 puzzles for each size
        print(f"\nRunning for {num_puzzles} {size}x{size} puzzles...")

        # Generate and load puzzles
        puzzles = [generate_puzzle(size, i) for i in range(num_puzzles)]
        puzzle_list = [puzzle_reader(puzzle) for puzzle in puzzles]

        # Generate unique output file name
        result_file = os.path.join(output_dir, f"comparison_{num_puzzles}_{size}x{size}.txt")

        # Compare algorithms on the generated puzzles
        results = compare_all_puzzle(puzzle_list, output_file=result_file)

        # Generate dynamic graphs for the results
        generate_dynamic_graphs(results, num_puzzles, size)
        print(f"Results saved to {result_file}")


def compare_incremental_puzzles(output_dir="comparison_results"):
    """
    Run comparisons incrementally for puzzle sizes 3x3 to 6x6 and save results.

    Args:
        output_dir (str): Directory to save summary text files and graphs.
    """
    create_output_directory(output_dir)

    for size in range(3, 7):  # Increment puzzle sizes from 3x3 to 6x6
        run_incremental_comparisons(size, output_dir)


if __name__ == "__main__":
    compare_incremental_puzzles()
