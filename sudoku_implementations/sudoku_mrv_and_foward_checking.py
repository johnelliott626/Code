import copy

# Global variables that all functions can access.
EMPTY = None
INITIAL_DOMAIN = {1, 2, 3, 4, 5, 6, 7, 8, 9}
NUM_RECURSIVE_CALLS = 0

# Returns a 2D array representing the initial sudoku puzzle board.
def initial_state(start_board, domain_map):
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
    
    # Set the initial domain for each cell (variable) on the board to the initial domain set
    for i in range(9):
        for j in range(9):
            domain_map[(i, j)] = {1, 2, 3, 4, 5, 6, 7, 8, 9}

    # Propogate domain values for each cell that is assigned a value
    for i in range(9):
        for j in range(9):
            current_cell_value = board[i][j]
            # If the cell is not empty propogate values for all "neighbors" of that cell
            if current_cell_value != EMPTY:
                has_possible_solution = propagate_cell_value((i, j), current_cell_value, domain_map)

                # There is a domain with zero values left, so no solution
                if not has_possible_solution:
                    print("No solution")
                    return None
    
    # Return the initial board configuration
    return board

# Removes the value from all neighboring cells (same row, column, subgrid) to implement forward checking. 
def propagate_cell_value(cell, value, domain_map):
    cell_row = cell[0]
    cell_column = cell[1]

    # Iterate over all cells and their domains
    for current_cell, domain in domain_map.items():
        
        current_row = current_cell[0]
        current_column = current_cell[1]

        # If the current_cell is the input cell, skip this iteration
        if current_cell == cell:
            domain.clear()
            domain.add(value)
            continue

        # Remove values from the domain of all cells in the same row, column, subgrid
        if current_row == cell_row or current_column == cell_column or (current_row // 3 == cell_row // 3 and current_column // 3 == cell_column // 3):
            # If the value is in the domain of a "neighbor" cell's domain, remove it
            if value in domain:
                domain.remove(value)
                # If the domain has 0 values left, return failure so backtrack
                if len(domain) == 0:
                    return False
                
                # If the domain has only 1 value left, it must be selected and so call this function recursively
                if len(domain) == 1:
                    if not propagate_cell_value(current_cell, next(iter(domain)), domain_map):
                        return False
            
    # If all domains have values left, return true
    return True

# Returns a list of tuple pairs, indicating which vaiables are unassigned.
def get_unassigned_cells(sudoku_board):
    unassigned_cells = [(i, j) for i in range(9) for j in range(9) if sudoku_board[i][j] == EMPTY]
    return unassigned_cells

# Heuristic function that returns the most constrained cell/variable to assign next (Minimum Remaining Values/ Most Constrained Variable heuristic)
def get_most_constrained_cell(sudoku_board, unassigned_cells):
    cell_constraints_map = {cell : 0 for cell in unassigned_cells}
    for cell in unassigned_cells:
        cell_row_index = cell[0]
        cell_column_index = cell[1]

        row = sudoku_board[cell_row_index]
        column = [sudoku_board[row_index][cell_column_index] for row_index in range(9)]

        subgrid_start_row = (cell_row_index // 3) * 3
        subgrid_start_column = (cell_column_index // 3) * 3
        subgrid = [sudoku_board[row_index][col_index] for row_index in range(subgrid_start_row, subgrid_start_row + 3) for col_index in range(subgrid_start_column, subgrid_start_column + 3)]

        # Increment the number of constraints on the current cell
        cell_constraints_map[cell] += sum(1 for element in row if element != EMPTY)
        cell_constraints_map[cell] += sum(1 for element in column if element != EMPTY)
        cell_constraints_map[cell] += sum(1 for element in subgrid if element != EMPTY)
            
    # Return the unnassigned cell that has the max number of constraints
    return max(cell_constraints_map, key=cell_constraints_map.get)

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
def backtrack(sudoku_board, domain_map):
    # Increment the number of recursive calls to this function.
    global NUM_RECURSIVE_CALLS
    NUM_RECURSIVE_CALLS += 1

    # If the sudoku board is complete then return it
    if goal_test(sudoku_board):
        return sudoku_board
    
    # Select the next unassigned cell to be assigned. General backtracking without any heuristic will just select the next varaiable.
    unassigned_cells = get_unassigned_cells(sudoku_board)
    cell_to_assign = get_most_constrained_cell(sudoku_board, unassigned_cells)
    
    # For each possible value in the cell's domain
    for value in domain_map[cell_to_assign]:
        # Get the updated board.
        new_sudoku_board = result(sudoku_board, cell_to_assign, value)

        # Create a copy of the domain map to pass down the recursion tree, in case we need to backtrack.
        domain_map_copy = copy.deepcopy(domain_map)

        # Check if the resulting board is consistent and that there is a possible variable assingment solution by propagating the cell with the value.
        if constraint_test(new_sudoku_board) and propagate_cell_value(cell_to_assign, value, domain_map_copy):
            # Recursively update the next cell on the board until a solution is found
            solution_board = backtrack(new_sudoku_board, domain_map_copy)

            # If the solution_board is not a failure return it otherwise backtrack.
            if solution_board is not None:
                return solution_board
    
    # If no solution is found (inability to satisfy all constraints based on current assignment) then return failure
    return None

# Returns the sudoku board solution that would result from the given board being solved.
def get_sudoku_solution(board):
    domain_map = dict()
    initial_board = initial_state(board, domain_map)
    if initial_board is None:
        return None
    solution_board = backtrack(initial_board, domain_map)
    return solution_board