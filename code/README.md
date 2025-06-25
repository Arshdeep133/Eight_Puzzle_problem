# **Multi-Agent Path Finding (MAPF) Project**

This project focuses on solving the Multi-Agent Path Finding (MAPF) problem using various search algorithms, including **BFS**, **DFS**, **A\*** with heuristics, **Greedy Best-First Search**, **IDA\***, and additional advanced heuristics like **Symmetry** and **Dual Lookup**. The project also includes features like puzzle generation, visualization of solving steps, and performance comparisons.

---

## **Table of Contents**

1. [Demo](#demo)  
2. [Installation](#installation)  
3. [Reproducing this Project](#repro)  
4. [Important Notes](#important-notes)  
5. [Troubleshooting](#troubleshooting)

---

<a name="demo"></a>
## **1. Demo - Generating and Solving MAPF Instances**

### **Generating Random Puzzles**

1. Generate an `n*n` solvable puzzle:
   ```bash
   python main.py 3
   ```
   This generates a 3x3 solvable puzzle and saves it to the `instances/generated_puzzle` directory.

### **Solving Puzzles with Algorithms**

1. Solve a specific puzzle using an algorithm:
   ```bash
   python main.py <file_path> <algorithm> [<heuristic>]
   ```
   Example:
   ```bash
   python main.py ./instances/sample_puzzle.txt a_star manhattan
   ```
   - Supported algorithms: `bfs`, `dfs`, `a_star`, `greedy`, `ida_star`, `reverse_bfs`
   - Supported heuristics (for A\*, Greedy): `manhattan`, `misplaced`, `symmetry`, `dual_lookup`

2. Solve using all algorithms:
   ```bash
   python main.py ./instances/sample_puzzle.txt all
   ```

### **Visualizing Puzzle Steps**

The program visualizes the solving steps dynamically:
- Each move is animated with colored tiles and grid borders.
- Final solutions, including the number of steps, are displayed.

---

<a name="installation"></a>
## **2. Installation**

To run this project, set up your environment as follows:

### **Prerequisites**
- **Python 3.10+**
- `pip` (Python package manager)

### **Steps**

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/<YourRepo>/MAPF_Project.git
   cd MAPF_Project
   ```

2. **Set Up Virtual Environment**:
   ```bash
   python -m venv .venv
   ```

3. **Activate Virtual Environment**:
   - On Windows:
     ```bash
     .\.venv\Scripts\activate
     ```
   - On Mac/Linux:
     ```bash
     source .venv/bin/activate
     ```

4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   **Dependencies** include:
   - `matplotlib`
   - `numpy`
   - `scipy`
   - `flask`
   - `Flask-Cors`

5. **Verify Installation**:
   ```bash
   python -c "import matplotlib, numpy, scipy, flask; print('All dependencies are installed.')"
   ```

---

<a name="repro"></a>
## **3. Reproducing this Project**

### **Step 1: Generate a Puzzle**

1. Use the `puzzle_generator` to generate an `n*n` solvable puzzle:
   ```bash
   python main.py 3
   ```

### **Step 2: Solve the Puzzle**

1. Solve the puzzle using an algorithm and heuristic:
   ```bash
   python main.py ./instances/generated_puzzle/random_generated_3x3.txt a_star dual_lookup
   ```

2. Solve and compare all algorithms:
   ```bash
   python main.py ./instances/generated_puzzle/random_generated_3x3.txt all
   ```

### **Step 3: Analyze Results**

- The output will display:
  - The solution path.
  - Number of steps.
  - Execution time.
- Visualized solving steps will appear as an animated grid.

---

<a name="important-notes"></a>
## **4. Important Notes**

1. **Puzzle Generator**:
   - The `puzzle_generator` guarantees only **solvable puzzles**.
   - Generated puzzles are stored in:
     ```
     ./instances/generated_puzzle/
     ```

2. **Algorithms**:
   - Algorithms supported:
     - BFS
     - DFS
     - A\* (Manhattan, Misplaced, Symmetry, Dual Lookup)
     - Greedy Best-First
     - IDA\*
     - Reverse BFS

3. **Heuristics**:
   - Heuristics for A\* and Greedy:
     - `manhattan`: Sum of Manhattan distances.
     - `misplaced`: Number of misplaced tiles.
     - `symmetry`: Uses symmetric transformations to reduce redundant states.
     - `dual_lookup`: Combines forward and backward Pattern Database (PDB) lookups.

---

<a name="troubleshooting"></a>
## **5. Troubleshooting**

### **Common Issues**

1. **ModuleNotFoundError**:
   - Ensure dependencies are installed:
     ```bash
     pip install -r requirements.txt
     ```

2. **"Puzzle Not Solvable" Error**:
   - The input puzzle may not be solvable. Use the generator to ensure solvability:
     ```bash
     python main.py 4
     ```

3. **Visualization Does Not Show**:
   - Make sure Matplotlib is installed and up to date:
     ```bash
     pip install matplotlib --upgrade
     ```

4. **Infinite Loops in DFS**:
   - The DFS implementation uses a visited set to avoid revisiting states. If issues persist, increase the timeout threshold or test smaller puzzles:
     ```bash
     python main.py ./instances/sample_puzzle.txt dfs
     ```

---

### **Contact**
For additional questions or support, reach out to the project maintainers.

---
