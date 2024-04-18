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

# Print sudoku puzzle in format of a sudoku puzzle.
def print_board(board):
    sudoku_board = [[str(element) if (element != 0 and element is not None) else "*" for element in row] for row in board]
    for i, row in enumerate(sudoku_board):
        if i % 3 == 0:
            print("+-------+-------+-------+")
        formatted_row = []
        for j, element in enumerate(row):
            if j % 3 == 0:
                formatted_row.append("| " + element)
            else:
                formatted_row.append(element)
        formatted_row.append("|")
        print(' '.join(formatted_row))
    print("+-------+-------+-------+")

# Get user input.
def get_integer_input(prompt, min_value, max_value):
    while True:
        try:
            value = int(input(prompt))
            if min_value <= value and value <= max_value:
                return value
            else:
                print(f"Invalid input. Input must be between {min_value} and {max_value}. Try again.")
        except ValueError:
            print("Invalid input. Please enter an integer.")



# Start of program
puzzles = read_sudoku_file("input.txt")

# Select a puzzle to solve.
puzzle_id = get_integer_input(f"Enter a puzzle number (1-{len(puzzles)}) from 'input.txt' to solve: ", 1, len(puzzles))
board = puzzles[puzzle_id]
print("\nInitial board: ")
print_board(board)

algorithms = {
    1: "Basic Backtracking",
    2: "Backtracking with MRV (Minimun Remaining Values) Heuristic",
    3: "Backtracking with Forward Checking",
    4: "Backtracking with MRV and Forward Checking",
    5: "Run all Algorithms above and compare"
}

# Select an algorithm to solve the puzzle.
propmt = f"""
Algorithm Options:
1 - {algorithms[1]}
2 - {algorithms[2]}
3 - {algorithms[3]}
4 - {algorithms[4]}
5 - {algorithms[5]}
Enter which algorithm to solve the sudoku puzzle from the above options:"""
algorithm_id = get_integer_input(propmt, 1, 5)


print("\nThinking...\n")

# Run the solution algorithms depending on user input.
if algorithm_id == 5:
    solution1 = sudoku_backtracking.get_sudoku_solution(board)
    states_explored1 = sudoku_backtracking.NUM_RECURSIVE_CALLS
    solution2 = sudoku_mrv.get_sudoku_solution(board)
    states_explored2 = sudoku_mrv.NUM_RECURSIVE_CALLS
    solution3 = sudoku_forward_checking.get_sudoku_solution(board)
    states_explored3 = sudoku_forward_checking.NUM_RECURSIVE_CALLS
    solution4 = sudoku_mrv_and_foward_checking.get_sudoku_solution(board)
    states_explored4 = sudoku_mrv_and_foward_checking.NUM_RECURSIVE_CALLS

    # Output the solutions
    same_solutions = True if solution1 == solution2 == solution3 == solution4 else False
    if same_solutions:
        print("Same solution for all algorithms.")
        print("Solution:")
        print_board(solution1)
    else:
        print("Different solutions found.")
        print("Solutions:")
        print("\nBacktracking solution:")
        print_board(solution1)
        print("\nMRV solution:")
        print_board(solution2)
        print("\nForward Checking solution:")
        print_board(solution3)
        print("\nMRV and Forward Checking solution:")
        print_board(solution4)

    # Output the number of states explored as a table.
    table_data = [["Puzzle Number", "Backtracking", "MRV", "Forward Checking", "MRV and Forward Checking", "Equivalent Solutions?"]]
    table_data.append([puzzle_id, states_explored1, states_explored2, states_explored3, states_explored4, "Yes" if solution1 == solution2 == solution3 == solution4 else "No"])
    print("Number of States Explored by Algorithm:")
    print(tabulate(table_data, headers="firstrow", tablefmt='fancy_grid'))
else: 
    if algorithm_id == 1:
        solution = sudoku_backtracking.get_sudoku_solution(board)
        states_explored = sudoku_backtracking.NUM_RECURSIVE_CALLS
    elif algorithm_id == 2:
        solution = sudoku_mrv.get_sudoku_solution(board)
        states_explored = sudoku_mrv.NUM_RECURSIVE_CALLS
    elif algorithm_id == 3:
        solution = sudoku_forward_checking.get_sudoku_solution(board)
        states_explored = sudoku_forward_checking.NUM_RECURSIVE_CALLS
    elif algorithm_id == 4:
        solution = sudoku_mrv_and_foward_checking.get_sudoku_solution(board)
        states_explored = sudoku_mrv_and_foward_checking.NUM_RECURSIVE_CALLS
    # Output results
    print(f"Algorithm selected: {algorithms[algorithm_id]}")
    print("Solution:")
    print_board(solution)
    print(f"Number of States Explored: {states_explored}")

