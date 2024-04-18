import copy

# Global variables that all functions can access.
EMPTY = None
INITIAL_DOMAIN = {1, 2, 3, 4, 5, 6, 7, 8, 9}
NUM_RECURSIVE_CALLS = 0

# Returns a 2D array representing the initial sudoku puzzle board.
def initial_state(start_board):
    board = [
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY]
    ]

    # Initialize the number of recursive calls to 0
    global NUM_RECURSIVE_CALLS
    NUM_RECURSIVE_CALLS = 0

    # Assign the board to the board passed as a parameter
    for i in range(9):
        for j in range(9):
            if start_board[i][j] != 0:
                board[i][j] = start_board[i][j]
    
    # Ensure the initial board configuration is consistent.
    if not constraint_test(board):
        return None
    
    # Return the initial board configuration
    return board

# Returns a list of tuple pairs, indicating which vaiables are unassigned.
def get_unassigned_cells(sudoku_board):
    unassigned_cells = [(i, j) for i in range(9) for j in range(9) if sudoku_board[i][j] == EMPTY]
    return unassigned_cells

# Returns the sudoku board that would result from the given cell being assigned the given value.
def result(sudoku_board, cell, value):
    new_sudoku_board = copy.deepcopy(sudoku_board)
    new_sudoku_board[cell[0]][cell[1]] = value
    return new_sudoku_board

# Returns True if the given board is a valid solution board, False otherwise
def goal_test(sudoku_board):
    # 1. Test if the assignment is complete (when every variable is assigned a value).
    for i in range(9):
        for j in range(9):
            if sudoku_board[i][j] == EMPTY:
                # Return False because there is an unassigned cell
                return False
            
    # 2. Test if all constraints are satisfied.
    return constraint_test(sudoku_board)

# Return True if the given board doesn't violate any constraints, False otherwise
def constraint_test(sudoku_board):
    # 1. Test each row in the sudoku board to see if it satisfies all constraints.
    for row in sudoku_board:
        row_list = [cell for cell in row if cell is not EMPTY]
        row_set = set(row_list)
        if len(row_list) != len(row_set):
            return False
        
    # 2. Test each column in the sudoku board to see if it satisfies all constraints.
    columns = [[row[column_index] for row in sudoku_board] for column_index in range(9)]
    for column in columns:
        column_list = [cell for cell in column if cell is not EMPTY]
        column_set = set(column_list)
        if len(column_list) != len(column_set):
            return False

    # 3. Test each of the 9 3x3 subgrids to see if it satisfies all constraints.
    subgrids = []
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            subgrid = [row[j:j+3] for row in sudoku_board[i:i+3]]
            subgrid = [cell for three_element_list in subgrid for cell in three_element_list]
            subgrids.append(subgrid)
    for subgrid in subgrids:
        subgrid_list = [cell for cell in subgrid if cell != EMPTY]
        subgrid_set = set(subgrid_list)
        if len(subgrid_list) != len(subgrid_set):
            return False
    
    # 4. Return True because all constraints are satisfied
    return True

# Backtrack algorithm that solves the sudoku board
def backtrack(sudoku_board):
    # Increment the number of recursive calls to this function.
    global NUM_RECURSIVE_CALLS
    NUM_RECURSIVE_CALLS += 1

    # If the sudoku board is complete then return it
    if goal_test(sudoku_board):
        return sudoku_board
    
    # Select the next unassigned cell to be assigned. General backtracking without any heuristic will just select the next varaiable.
    unassigned_cells = get_unassigned_cells(sudoku_board)
    cell_to_assign = unassigned_cells[0]
    
    # For each possible value in the cell's domain
    for value in INITIAL_DOMAIN:
        # Check if the resulting board is consistent (satisifies all constraints)
        new_sudoku_board = result(sudoku_board, cell_to_assign, value)
        if constraint_test(new_sudoku_board):
            # Recursively update the next cell on the board until a solution is found
            solution_board = backtrack(new_sudoku_board)

            # If the solution_board is not a failure return it otherwise backtrack.
            if solution_board is not None:
                return solution_board
    
    # If no solution is found (inability to satisfy all constraints based on current assignment) then return failure
    return None

# Returns the sudoku board solution that would result from the given board being solved.
def get_sudoku_solution(board):
    initial_board = initial_state(board)
    if initial_board is None:
        return None
    solution_board = backtrack(initial_board)
    return solution_board