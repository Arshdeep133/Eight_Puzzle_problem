from itertools import permutations
from collections import Counter, deque
import algorithms.reverse_bfs as rv
import numpy as np

def save_pdb(pdb, filename):
    with open(filename, 'w') as file:
        for state, cost in pdb:
            file.write(f"{state}: {cost}\n")

def load_pdb(filename):
    pdb = []
    with open(filename, 'r') as file:
        for line in file:
            state_str, cost_str = line.strip().split(": ")
            state = eval(state_str) 
            cost = int(cost_str)
            pdb.append((state, cost))
    return pdb

def create_disjoint_pdb(n):
    all_group = []
    if n == 3:
        #grouped_tiles = disjointset1(n)
        grouped_tiles = disjointset2(n)
        for group in grouped_tiles:
            pdb = precompute_pdb(group, n)
            all_group.extend(pdb.items())
        #save_pdb(all_group, "disjoint_pdb3.txt")
        save_pdb(all_group, "disjoint_pdb3_1.txt")
    elif n == 4:
        #grouped_tiles = disjointset1(n)
        grouped_tiles = disjointset3(n)
        for group in grouped_tiles:
            pdb = precompute_pdb(group, n)
            all_group.extend(pdb.items())
        #save_pdb(all_group, "disjoint_pdb4.txt")
        save_pdb(all_group, "disjoint_pdb4_1.txt")

def precompute_pdb(group, n):
    pdb = {}
    flattened = flatten_2d_array(group)
    all_states = unique_permutations(flattened)
    for states in all_states:
        pdb[states] = rv.reverse_bfs(states, n)
    return pdb

# convert 2D array to 1D
def flatten_2d_array(group):
    return [item for sublist in group for item in sublist]


# considering all duplicate elements as 1
def unique_permutations(sequence):
    unique_perms = set(permutations(sequence))
    return list(unique_perms)

def disjointset1(n):
    #n n n-1 disjoint set
    #The blank tile (0) is not part of the group.
    #During reverse BFS the blank tile is dynamically allowed to occupy any position in the puzzle
    #So, any tiles marked -1 can be used as blank tiles
    group_tile = [[[-1 for _ in range(n)] for _ in range(n)] for _ in range(n)]
    empty = None
    state = [[(i * n + j + 1) % (n * n) for j in range(n)] for i in range(n)]
    for i in range(n):
        for row in range(n):
            for col in range(n):
                if row == i and state[row][col] != 0:
                    group_tile[i][row][col] = state[row][col]
    return group_tile

def disjointset2(n):
    #4 - 4 disjoint set for 8 puzzle
    group_tile = [[[1 , 2, -1],[4 , 5 ,-1], [-1, -1, -1]], [[-1 , -1, 3],[-1 , -1 , 6], [7, 8, -1]]]
    return group_tile

def disjointset3(n):
    #8 - 7 disjoint set for 15 puzzle
    group_tile = [[[1 , 2, 3, -1],[5 , 6 , 7, -1], [9, 10, 11, -1], [-1 , -1, -1, -1]], [[-1 , -1,-1, 4],[-1 , -1 , -1, 8], [-1, -1, -1, 12], [13 , 14, 15, -1]]]
    return group_tile