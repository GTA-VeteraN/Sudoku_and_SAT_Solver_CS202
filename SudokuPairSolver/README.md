# Sudoku Pair Solver 
SudokuSolver.py
- Python file to solve for sudoku pair

<strong>Input</strong> :  The filename (if file in same folder) / pathname of the csv file (Ex - test79883.csv , ./test/test79883.csv)
The parameter k is automatically calculated using the csv file itself.</br>

<strong>Output</strong> : The Sudoku pair.
Format of Output : 'Sudoku 1' then in the new line k*k rows with k*k cells for first Sudoku.
                   'Sudoku 2' then in the new line k*k rows with k*k cells for second Sudoku.

## Implementation:
1. We have implemented minimal encoding in which exactly one condition is used only while constraining the 
values in each cell rather than using this condition for row, column and block constraints which would increase the 
number of clause. For row, column and block constraints we have used only the constraint that each one of them is 
assigned a valid number( Point 1 of Constaints for graph coloring in Lecture Slides )
2. For k=2 we had 384 clauses and for k=3 we had 7209 clauses excluding the constraints from the csv file.
3. After that we have added the constraints for sudoku pair and constraints that we got from the csv file.
4. We have converted the values to the variables using the formula i*N*N + j*N + k +1 so that we can easily recover 
them by just using modulus with N.
5. We have used the Cadical SAT Solver for solving and the CNF module to store the clauses.


# Sudoku Pair Generator
SudokuPair_Generator.py
- Python file to generate Sudoku pair

Input : The Suduko dimension parameter k.</br>
Output : A csv file named test{random number between 1 to 100000}.csv ( Ex - test14586.csv) 
Format of the Output : First k rows with kxk cells each for the first sudoku and the rest of the rows for the 
second sudoku.  Cell with 0 specifies an empty cell.

## Implementation:
1. For generating the sudoku pair, we have implemented extended encoding for solving the sudoku pair
in which 'exactly_one' condition is used while constraining the values for each row, column and block. This has
increased the number of clauses but has reduced the time significantly. We first tried using minimal encoding 
with less number of clauses but it took a lot of time so we shifted to extended encoding.
2. For generating the sudoku pair with maximal holes and unique solution we have used the Naive Model Counting 
method discussed in the live class( Actually We had already implemented it before the live lecture ).
3. In the method we randomly choose a position and assigned it a random value ( So as to generate unique sudoku
pair every time) and then solve the sudoku pair, after that every time we remove a value from a random position and 
check whether the sudoku pair now has a unique solution( by adding another clause that is negation of the model we 
get in the previous step) and when we get a sudoku pair which has two or more solution, we stop and the sudoku pair
just before this step is the final answer. 


# Assumptions:
For SudokuPair_Generator.py:
As the dimension of sudoku pair increases, some number of holes will always be there in the generated sudoku pair,
so we exploited this fact. After doing some testing for cases k=4 , k=5 we assumed the following:
1. For k=4 , we were always getting the number of holes > 80 for the unique sudoku pair.
So in order to reduce the time taken for generating the 16x16 sudoku pair, we randomly removed 80 terms 
without even checking for the unique solution as it would always happen and after that we started checking for
the unique solution.( using SudokuSolver.py). This reduced time drastically and gave correct results upto
our knowledge.
2. For k=5 , we similarly removed first 200 terms.

# Limitations:
1. The Sudoku generator was not working better before the assumptions we made for k=4 and k=5. Taking in the 
assumption can compromise the result. But we did some good amount of testing before coming to this assumption.
We think that the condition of maximal number of holes and uniqueness of sudoku pair will be fulfilled every time 
the sudoku pair is generated.



