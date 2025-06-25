import time
import tracemalloc
from utils.puzzle_solver import puzzle_reader, solve_puzzle
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.reverse_bfs import reverse_bfs
from algorithms.astar import a_star
from algorithms.bidirectional import bidirectional_search
from algorithms.iddfs import iddfs
from algorithms.greedy import greedy
from algorithms.heuristics import generate_dual_pdbs, generate_pdb
import matplotlib.pyplot as plt
import os

from algorithms.idastar import ida_star

ALGORITHMS = {
        "bfs": bfs,
        # "dfs": dfs,
        "a_star": a_star,
        "bidirectional": bidirectional_search,
        "iddfs": iddfs,
        "greedy": greedy,
        "ida_star": ida_star,
        "reverse_bfs": reverse_bfs
        # Add more algorithms here as needed
    }

HEURISTICS = ["manhattan", "misplaced", "linear_conflict", "inconsistent", "non_additive_pdb", "symmetry", "dual_lookup", "disjointpdb"]

HEURISTICS = ["non_additive_pdb", "dual_lookup", "disjointpdb"]

def solve_and_visualize(puzzle, algorithm, heuristic, pdbs):
    solution_path = None
    try:
        tracemalloc.start()
        start_time = time.perf_counter()
        solution_path = solve_puzzle(puzzle, algorithm, ALGORITHMS, heuristic, pdbs)
        end_time = time.perf_counter()
        memory_usage, _ = tracemalloc.get_traced_memory()
        execution_time = end_time - start_time
        completeness = "Yes" if solution_path else "No"
        solution_length = len(solution_path) - 1 if solution_path else "N/A"
        optimality = "Yes" if solution_path and solution_length <= len(a_star(puzzle, heuristic="manhattan")) - 1 else "No"
        tracemalloc.stop()
        result = {
                    "Execution Time (s)": execution_time,
                    "Memory Usage (KB)": memory_usage / 1024,
                    "Completeness": completeness,
                    "Solution Steps": solution_length,
                    "Optimality": optimality
                }
    except Exception as e:
        end_time = time.perf_counter()
        tracemalloc.stop()
        result = {
            "Execution Time (s)": end_time - start_time,
            "Memory Usage (KB)": "N/A",
            "Completeness": "Error",
            "Solution Steps": "N/A",
            "Optimality": "N/A",
            "Error": str(e)
        }

    if solution_path:
        print(result)
        #visualize_puzzle_solution(solution_path)
    else:
        print(f"No solution found for {algorithm.upper()}.")

    return result

def save_summary_to_file(filename, puzzle, algorithm_results, overall_results=None, best_algorithm=None, conclusion=None):
    """
    Saves a summary of the results to a text file.

    Args:
        filename (str): The name of the output file.
        puzzle (list): The specific puzzle tested.
        algorithm_results (dict): Results of algorithms on the specific puzzle.
        overall_results (dict, optional): Aggregated results across all puzzles.
        best_algorithm (str, optional): The best algorithm across all puzzles.
        conclusion (str, optional): Final conclusion about the overall performance.
    """
    with open(filename, "w") as file:
        file.write("=== Puzzle Summary ===\n")
        file.write("Puzzle:\n")
        for row in puzzle:
            file.write(" ".join(map(str, row)) + "\n")
        file.write("\n=== Algorithm Results ===\n")
        for algo, metrics in algorithm_results.items():
            file.write(f"{algo}:\n")
            for key, value in metrics.items():
                file.write(f"  {key}: {value}\n")
            file.write("\n")

        if overall_results:
            file.write("\n=== Overall Performance Across All Puzzles ===\n")
            for algo, metrics in overall_results.items():
                file.write(f"{algo}:\n")
                for key, value in metrics.items():
                    file.write(f"  {key}: {value}\n")
                file.write("\n")
        
        if best_algorithm:
            file.write(f"Best Algorithm: {best_algorithm}\n")

        if conclusion:
            file.write(f"\n=== Conclusion ===\n{conclusion}\n")
        
        file.write("\n=== End of Report ===\n")

def compare_algorithms(puzzle, output_file="tests/algorithm_results.txt"):
    """
    Compares the performance of different search algorithms on the given puzzle.

    Args:
        puzzle (list): The initial puzzle state as a 2D list.

    Returns:
        dict: A dictionary containing performance metrics for each algorithm.
    """
    n = len(puzzle)
    results = {}
    non_additive_pdbs = generate_pdb(puzzle, len(puzzle))
    goal = [[(i * n + j + 1) % (n * n) for j in range(n)] for i in range(n)]
    dual_pdbs = generate_dual_pdbs(puzzle, goal , goal)
    for algorithm in ALGORITHMS:
        if algorithm in ["a_star", "greedy", "ida_star"]:
            for heuristic in HEURISTICS:
                print(f"\nVisualizing solution for {algorithm.upper()}({heuristic.upper()}) algorithm:")
                if heuristic == "dual_lookup":
                    results[algorithm+"_"+heuristic] = solve_and_visualize(puzzle, algorithm, heuristic, dual_pdbs)
                elif heuristic == "non_additive_pdb":
                    results[algorithm+"_"+heuristic] = solve_and_visualize(puzzle, algorithm, heuristic, non_additive_pdbs)
                else:
                    results[algorithm+"_"+heuristic] = solve_and_visualize(puzzle, algorithm, heuristic, None)
        else:
            print(f"\nVisualizing solution for {algorithm.upper()} algorithm:")
            results[algorithm] =   solve_and_visualize(puzzle, algorithm, None, None)
    
    optimal_results = {k: v for k, v in results.items() if v["Optimality"] == "Yes"}
    if optimal_results:
        best_algorithm = min(
            optimal_results,
            key=lambda x: (
                results[x]["Execution Time (s)"],
                results[x]["Memory Usage (KB)"],
                results[x]["Solution Steps"] if results[x]["Completeness"] == "Yes" else float("inf"),
            ),
        )
    else:
         best_algorithm = None
    print(f"Best Algorithm for the Current Puzzle: {best_algorithm}")

    conclusion = f"The best algorithm for this puzzle is {best_algorithm}, as it provided the most efficient solution."

    save_summary_to_file(output_file, puzzle, results, conclusion=conclusion)


    return results


def compare_all_puzzle(all_puzzles,  output_file="tests/algorithm_results.txt"):
    """
    Runs all algorithms on a collection of puzzles and calculates overall performance.

    Args:
        all_puzzles (list): A list of puzzles (each as a 2D list).

    Returns:
        dict: Aggregated results across all puzzles.
    """

    overall_results = {}
    for algo in ALGORITHMS:
        if algo in ["a_star", "greedy", "ida_star"]:  # For algorithms that use heuristics
            for heuristic in HEURISTICS:
                key = f"{algo}_{heuristic}"  # Create a unique key for each algorithm-heuristic combination
                overall_results[key] = {
                    "Total Execution Time (s)": 0, 
                    "Success Count": 0, 
                    "Memory Usage (KB)": 0,
                    "Optimality":0,
                    "Total Puzzles": len(all_puzzles)
                }
        else:  # For algorithms that don't use heuristics
            overall_results[algo] = {
                "Total Execution Time (s)": 0, 
                "Success Count": 0, 
                "Memory Usage (KB)":0,
                "Optimality":0,
                "Total Puzzles": len(all_puzzles)
            }
    all_individual_results = {}
    for idx, puzzle in enumerate(all_puzzles):
        print(f"Running algorithms on puzzle {idx + 1}...")
        individual_results = {}
        n = len(puzzle)
        non_additive_pdbs = generate_pdb(puzzle, len(puzzle))
        goal = [[(i * n + j + 1) % (n * n) for j in range(n)] for i in range(n)]
        dual_pdbs = generate_dual_pdbs(puzzle, goal , goal)
        for algorithm in ALGORITHMS:
            if algorithm in ["a_star", "greedy", "ida_star"]:
                for heuristic in HEURISTICS:
                    print(f"\nVisualizing solution for {algorithm.upper()}({heuristic.upper()}) algorithm:")
                    if heuristic == "dual_lookup":
                        individual_results[algorithm+"_"+heuristic] = solve_and_visualize(puzzle, algorithm, heuristic, dual_pdbs)
                    elif heuristic == "non_additive_pdb":
                        individual_results[algorithm+"_"+heuristic] = solve_and_visualize(puzzle, algorithm, heuristic, non_additive_pdbs)
                    else:
                        individual_results[algorithm+"_"+heuristic] = solve_and_visualize(puzzle, algorithm, heuristic, None)
                    print(individual_results[algorithm+"_"+heuristic])
                    overall_results[algorithm+"_"+heuristic]["Total Execution Time (s)"] += individual_results[algorithm+"_"+heuristic]['Execution Time (s)']
                    if individual_results[algorithm+"_"+heuristic]["Memory Usage (KB)"] != 'N/A':
                        overall_results[algorithm+"_"+heuristic]["Memory Usage (KB)"] += individual_results[algorithm+"_"+heuristic]['Memory Usage (KB)']
                    if individual_results[algorithm+"_"+heuristic]['Completeness'] == "Yes":
                        overall_results[algorithm+"_"+heuristic]["Success Count"] += 1
                    if individual_results[algorithm+"_"+heuristic]['Optimality'] == "Yes":
                        overall_results[algorithm+"_"+heuristic]["Optimality"] += 1
            else:
                print(f"\nVisualizing solution for {algorithm.upper()} algorithm:")
                individual_results[algorithm] =  solve_and_visualize(puzzle, algorithm, None, None)
                overall_results[algorithm]["Total Execution Time (s)"] += individual_results[algorithm]['Execution Time (s)']
                if individual_results[algorithm]["Memory Usage (KB)"] != 'N/A':
                    overall_results[algorithm]["Memory Usage (KB)"] += individual_results[algorithm]['Memory Usage (KB)']
                if individual_results[algorithm]['Completeness'] == "Yes":
                    overall_results[algorithm]["Success Count"] += 1
                if individual_results[algorithm]['Optimality'] == "Yes":
                        overall_results[algorithm]["Optimality"] += 1

        all_individual_results[f"Puzzle {idx + 1}"] = {
            "Puzzle": puzzle,
            "Results": individual_results
        }

    # Calculate average execution time and success rate
    for name, metrics in overall_results.items():
        metrics["Average Execution Time (s)"] = (
            metrics["Total Execution Time (s)"] / metrics["Total Puzzles"]
        )
        metrics["Average Memory Usage (KB)"] = (
            metrics["Memory Usage (KB)"] / metrics["Total Puzzles"]
        )
        metrics["Success Rate"] = metrics["Success Count"] / metrics["Total Puzzles"]
        metrics["Optimality Rate"] = metrics["Optimality"] / metrics["Total Puzzles"]

    # Determine the best algorithm across all puzzles
    optimal_overall_results = {k: v for k, v in overall_results.items() if v["Optimality Rate"] == 1}
    if optimal_overall_results:
        best_algorithm_overall = max(
            optimal_overall_results,
            key=lambda x: (
                overall_results[x]["Success Rate"], 
                -overall_results[x]["Average Execution Time (s)"], 
                -overall_results[x]["Average Memory Usage (KB)"],
            ),
                
        )
    else: 
        best_algorithm_overall = None
    print(f"Best Algorithm Across All Puzzles: {best_algorithm_overall}")

    conclusion = f"The best algorithm across all puzzles is {best_algorithm_overall}, balancing success rate and execution time."

    # Save all results to the output file
    with open(output_file, "w") as file:
        file.write("=== Individual Puzzle Results ===\n")
        for puzzle_id, details in all_individual_results.items():
            file.write(f"{puzzle_id}:\n")
            file.write("Puzzle:\n")
            for row in details["Puzzle"]:
                file.write(" ".join(map(str, row)) + "\n")
            file.write("\nAlgorithm Results:\n")
            for algo, metrics in details["Results"].items():
                file.write(f"  {algo}:\n")
                for key, value in metrics.items():
                    file.write(f"    {key}: {value}\n")
                file.write("\n")
            file.write("\n")

        file.write("\n=== Overall Performance Across All Puzzles ===\n")
        for algo, metrics in overall_results.items():
            file.write(f"{algo}:\n")
            for key, value in metrics.items():
                file.write(f"  {key}: {value}\n")
            file.write("\n")

        file.write(f"\n=== Conclusion ===\n{conclusion}\n")
        file.write("\n=== End of Report ===\n")

    return overall_results

def generate_dynamic_graphs(overall_results, num_puzzles, size, output_dir="comparison_results"):
    """
    Generate graphs dynamically based on the overall results.

    Args:
        overall_results (dict): The aggregated performance results for all algorithms.
    """
    # List of algorithms (keys in the results dictionary)
    if not os.path.exists('tests'):
        os.makedirs('tests')
    file_name = os.path.join(output_dir, f"{num_puzzles}_{size}x{size}")
    algorithms = list(overall_results.keys())

    # Metrics to plot
    execution_times = [overall_results[algo]["Average Execution Time (s)"] for algo in algorithms]
    memory_usage = [overall_results[algo]["Average Memory Usage (KB)"] for algo in algorithms]
    success_rates = [overall_results[algo]["Success Rate"] for algo in algorithms]
    optimality_rates = [overall_results[algo]["Optimality Rate"] for algo in algorithms]

    # Plot Average Execution Time
    plt.figure(figsize=(10, 6))
    plt.barh(algorithms, execution_times, color='skyblue')
    plt.xlabel('Average Execution Time (s)')
    plt.title('Average Execution Time for Different Algorithms')
    plt.tight_layout()
    plt.savefig(f'{file_name}_average_execution_time.png')
    plt.close()

    # Plot Memory Usage
    plt.figure(figsize=(10, 6))
    plt.barh(algorithms, memory_usage, color='lightcoral')
    plt.xlabel('Average Memory Usage (KB)')
    plt.title('Memory Usage for Different Algorithms')
    plt.tight_layout()
    plt.savefig(f'{file_name}_average_memory_usage.png')
    plt.close()

    # Plot Success Rate
    plt.figure(figsize=(10, 6))
    plt.barh(algorithms, success_rates, color='lightgreen')
    plt.xlabel('Success Rate')
    plt.title('Success Rate for Different Algorithms')
    plt.tight_layout()
    plt.savefig(f'{file_name}_success_rate.png')
    plt.close()

    # Plot Optimality Rate
    plt.figure(figsize=(10, 6))
    plt.barh(algorithms, optimality_rates, color='lightskyblue')
    plt.xlabel('Optimality Rate')
    plt.title('Optimality Rate for Different Algorithms')
    plt.tight_layout()
    plt.savefig(f'{file_name}_optimality_rate.png')
    plt.close()