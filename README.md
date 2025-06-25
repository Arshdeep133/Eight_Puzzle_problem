# Search_Algorithm_Evaluation_System_on_3*3_Eight_puzzles
 
##Project Scope
This project focuses on evaluating and comparing various search algorithms—both uninformed and informed—for solving the 3×3 sliding tile puzzle, also known as the Eight Puzzle. The puzzle requires moving tiles into a goal configuration by sliding one tile at a time into the empty space. Due to the exponential growth of state space, the Eight Puzzle serves as an excellent benchmark for studying the efficiency and effectiveness of different search strategies and heuristics.

##Objectives:
Compare multiple uninformed and informed search algorithms

Evaluate different heuristic functions in guiding A* and IDA* searches

Analyze performance based on execution time, memory usage, solution optimality, and success rate

Visualize the solving process and enable batch testing of puzzle instances

## Libraries Required
The implementation is in Python 3.9.7 and uses the following standard libraries:

| Library        | Purpose                                                  |
|----------------|----------------------------------------------------------|
| numpy          | Efficient numerical operations and matrix manipulation   |
| time           | Tracking execution time for performance evaluation       |
| psutil         | Measuring memory usage during algorithm runs             |
| sys, os        | File system interaction and command-line support         |
| matplotlib     | Visualization of puzzle-solving process                  |
| itertools      | Generating permutations and combinations                 |
| heapq          | Priority queue implementation for A* and Greedy          |
| collections    | Data structures like `deque` used in BFS, DFS            |
| multiprocessing| Parallel execution for batch testing                     |


To install dependencies:

bash
Copy
Edit
pip install numpy psutil matplotlib

## Algorithms Implemented
### Uninformed (Blind) Search Algorithms
Breadth-First Search (BFS)
Depth-First Search (DFS)
Bidirectional BFS
Iterative Deepening DFS (IDDFS)

### Informed (Heuristic) Search Algorithms
A*

Uses f(n) = g(n) + h(n); optimal if heuristic is admissible and consistent

Greedy Best-First Search

Uses only h(n); fast but not guaranteed to be optimal

Iterative Deepening A* (IDA*)

Memory-efficient version of A*; uses threshold-based pruning

## Heuristics Used
Manhattan Distance

Sum of horizontal and vertical distances from target positions

Misplaced Tiles

Counts number of incorrectly placed tiles

Linear Conflict

Manhattan + penalty for conflicting tiles in the same row/column

Inconsistent Heuristic

Modified Manhattan that doubles penalty for even-numbered tiles (not consistent)

Pattern Databases (PDBs)

Precomputed optimal steps for subsets of tile positions

Variants used:

Non-additive PDB

Disjoint PDBs (e.g., 4-4, 3-3-2 tile splits)

Symmetry PDB (exploits mirrored state equivalence)

Dual Lookup (forward and backward PDBs combined)

## Evaluation Metrics
Execution Time (s)

Memory Usage (KB)

Success Rate (number of puzzles solved within timeout)

Optimality Rate (number of optimal solutions matched to A* with Misplaced Tiles)

