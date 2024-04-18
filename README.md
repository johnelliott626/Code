To run the program to find the solution of a sudoku puzzle.

Step 1:
Download the tabulate module and set your working directory:
In your terminal run the command: pip install tabulate
If not try instead (if you have Python2 and 3 on your machine): pip3 install tabulate
Ensure your current working directory is set to the project directory that contains the 'sudoku_solver.py' and 'input.txt' files

Step 2:
Look at the "input.txt" file to see all possible puzzles in the form:
<Grid #>
<value><value><value><value><value><value><value><value><value>
<value><value><value><value><value><value><value><value><value>
<value><value><value><value><value><value><value><value><value>
<value><value><value><value><value><value><value><value><value>
<value><value><value><value><value><value><value><value><value>
<value><value><value><value><value><value><value><value><value>
<value><value><value><value><value><value><value><value><value>
<value><value><value><value><value><value><value><value><value>
<value><value><value><value><value><value><value><value><value>
Note: Values of zero indicate which cells in the puzzle is empty.

Step 3:
In your terminal run the command: python sudoku_solver.py

Step 4:
Enter a puzzle number (1-50) from the 'input.txt' file to solve.

Step 5:
Enter which algorithm you would like to use to solve the puzzle. (Enter 1-5 as instructed by the program below).

Step 6:
Allow program to execute. And view output at the terminal.

Note: Source for provided txt file of sudoku puzzles: https://github.com/dimitri/sudoku/blob/master/sudoku.txt
