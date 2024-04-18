# Source for provided txt file of sudoku puzzles: https://github.com/dimitri/sudoku/blob/master/sudoku.txt

# Import functions from each implementation file.
from sudoku_implementations import sudoku_backtracking
from sudoku_implementations import sudoku_mrv
from sudoku_implementations import sudoku_forward_checking
from sudoku_implementations import sudoku_mrv_and_foward_checking
from tabulate import tabulate

# Read in each sudoku puzzle in the file and return them as a dictionary as PuzzleNumber: Puzzle values
def read_sudoku_file(filename):
    all_puzzles = dict()
    puzzle_number = 1
    with open(filename, 'r') as file:
        # Read in each line of the file.
        lines = file.readlines()

        for i in range(len(lines)):
            if lines[i].startswith('Grid'):
                puzzle_start_index = i + 1
                current_puzzle = [[int(char) for char in line.strip()] for line in lines[puzzle_start_index:puzzle_start_index + 9]]
                all_puzzles[puzzle_number] = current_puzzle
                puzzle_number += 1

    return all_puzzles

puzzles = read_sudoku_file("input.txt")
table_data = []
headers = ["Puzzle Number", "General Backtracking", "MRV Heuristic", "Forward Checking", "MRV and Forward Checking", "Equivalent Solutions?"]

# Test each file in the input file
for i in range(1, (len(puzzles) + 1)):
    board = puzzles[i]
    print(f"\nComputing Board {i}...\n")

    solution = sudoku_backtracking.get_sudoku_solution(board)
    solution_mrv = sudoku_mrv.get_sudoku_solution(board)
    solution_fk = sudoku_forward_checking.get_sudoku_solution(board)
    solution_mrv_fk = sudoku_mrv_and_foward_checking.get_sudoku_solution(board)

    if solution == solution_mrv == solution_fk == solution_mrv_fk:
        equivalent = "Yes"
    else: 
        equivalent = "No"

    table_data.append([i, sudoku_backtracking.NUM_RECURSIVE_CALLS, sudoku_mrv.NUM_RECURSIVE_CALLS, sudoku_forward_checking.NUM_RECURSIVE_CALLS, sudoku_mrv_and_foward_checking.NUM_RECURSIVE_CALLS, equivalent])

# Compute averages and output a table.    
backtracking_avg = sum(table_data[row_index][1] for row_index in range(len(table_data))) / len(table_data)
mrv_avg = sum(table_data[row_index][2] for row_index in range(len(table_data))) / len(table_data)
fc_avg = sum(table_data[row_index][3] for row_index in range(len(table_data))) / len(table_data)
mrv_fk_avg = sum(table_data[row_index][4] for row_index in range(len(table_data))) / len(table_data)

table_data.append(["Average", backtracking_avg, mrv_avg, fc_avg, mrv_fk_avg, "N/A"])
print(tabulate(table_data, headers=headers, tablefmt='fancy_grid'))
