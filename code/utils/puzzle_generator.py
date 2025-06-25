import random
import os
import time
def count_inversions(numbers):
    """Counts the number of inversions in the puzzle."""
    inversions = 0
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] > numbers[j] and numbers[i] != 0 and numbers[j] != 0:
                inversions += 1
    return inversions

def is_solvable(puzzle, n):
    """Checks if the puzzle is solvable."""
    numbers = [num for row in puzzle for num in row]  # Flatten the puzzle
    inversions = count_inversions(numbers)

    if n % 2 == 1:  # Odd grid size (e.g., 3x3)
        return inversions % 2 == 0
    else:  # Even grid size (e.g., 4x4)
        blank_row = next(i for i, row in enumerate(puzzle) if 0 in row)
        blank_row_from_bottom = n - blank_row
        return (inversions % 2 == 0) if blank_row_from_bottom % 2 == 1 else (inversions % 2 == 1)

def generate_solvable_puzzle(n):
    """Generates a solvable n*n puzzle."""
    while True:
        numbers = list(range(n * n))  # Numbers from 0 to n*n-1
        random.shuffle(numbers)       # Shuffle to randomize the puzzle
        puzzle = [numbers[i:i + n] for i in range(0, len(numbers), n)]
        if is_solvable(puzzle, n):
            return puzzle

def generate_puzzle(n, i):
    """Generates a random n*n solvable puzzle and saves it to a file.

    Args:
        n (int): The size of the puzzle (n x n).

    Returns:
        str: The file path where the puzzle is saved.
    """
    # Generate a solvable puzzle
    puzzle = generate_solvable_puzzle(n)

    # Ensure the output directory exists
    output_dir = "./instances/generated_puzzle"
    os.makedirs(output_dir, exist_ok=True)

    # Define the file name and path
    timestamp = int(time.time())
    file_name = f"random_generated_{n}x{n}_puzzle_{i}.txt"
    file_path = os.path.join(output_dir, file_name)

    # Save the puzzle to a file
    with open(file_path, "w") as file:
        for row in puzzle:
            file.write(" ".join(map(str, row)) + "\n")

    print(f"Generated solvable {n}x{n} puzzle and saved to {file_path}.")
    return file_path
