# This is the file for Sudoku Solver
# Input : You just need to enter the filename( if file in same folder) / pathname
# of the csv file( Ex - test79883.csv , ./test/test79883.csv)
# The parameter k is automatically calculated using the csv file itself
# Output : The Sudoku Pair along with the time taken for execution


# Importing important modules
import pysat
from pysat.formula import CNF 
from pysat.solvers import Cadical
import csv
import math
import time

# Taking filename as input for the csv file to be read
filename = input("Please enter the csv filename/pathname to read along with extension:")
file = open(filename)
start = time.time()
csvreader = csv.reader(file)
# Reading the data from the csv file
rows =[]
for row in csvreader:
    rows.append(row)
N = len(rows[0])
M = int(math.sqrt(N))
constraints = []
for i in range(2*N):
    for j in range(N):
        data = int(rows[i][j])
        if data: constraints.append([i,j,data])

# Function to make constraints of having exactly one value as mentioned in the lectures 
def exactly_one(variables):
    cnf = [ variables]
    n = len(variables)

    for i in range(n):
        for j in range(i+1,n):
            v1 = variables[i]
            v2 = variables[j]
            cnf.append([-v1,-v2])

    return cnf

# Naming the variables
def transform(i,j,k):
    return i*N*N + j*N + k + 1

# After getting the solution, we need to convert the variables back to the sudoku values
def inverse_transform(v):
    v,k = divmod(v-1, N)
    v,j = divmod(v, N)
    if( v >= N): (v,i) = divmod(v, 2*N)
    else : v,i = divmod(v, N)
    return i,j,k

if __name__ == '__main__':
    v1 =[] 
    v2 =[]
    formula = CNF()

    # Column and Row constraints for Sudoku Pair
    for i in range(N):
        for s in range(N):
            formula.append([transform(i,j,s) for j in range(N)])
            formula.append([transform(j,i,s) for j in range(N)])
            formula.append([transform(i+N,j,s) for j in range(N)])
            formula.append([transform(j , i , s) for j in range(N,2*N)])

        # For cell constraints that is exactly one value from 1 to N in each cell
        for j in range(N):
            v1 = v1 + exactly_one([transform(i,j,k) for k in range(N)])
            v2 = v2 +exactly_one([transform(i+N,j,k) for k in range(N)])

    # appending the cell constraints to the CNF formula     
    for z in v1:
        formula.append(z)
    for z in v2:
        formula.append(z)

    # Block Constraints, that is each MxM block should have number from 1 to N. 
    for k in range(N):
        for x in range(M):
            for y in range(M):
                v = [transform(y*M +i , x*M +j , k) for i in range(M) for j in range(M)] 
                v2 = [transform(y*M + N +i, x*M +j, k) for i in range(M) for j in range(M)]
                formula.append(v)                
                formula.append(v2)                

    # Sudoku Pair constraints that is Sudoku Pair should not have same value for same position
    for x in range(N):
        for y in range(N):
            for k in range(N):
                v1 = transform(x,y,k)
                v2 = transform(x+N, y, k)
                formula.append([-v1,-v2])
   
    # Adding the initial constraint from the csv file to the formula
    for z in constraints:
        formula.append([transform(z[0],z[1],z[2])-1])
    solution = []

    flag = True # For checking whether the formula is Satisfiable or not
    # Solving the clauses using Cadical SAT Solver
    with Cadical( bootstrap_with=formula.clauses) as c:
        if c.solve(): solution = c.get_model()
        else: flag = False
    final_ans =[]
    # If Model exists,  Extracting the solution that is positive values
    if flag:
        for z in solution:
            if z>0 :
                ans = inverse_transform(z) 
                final_ans.append(ans[2]+1)
        # Printing the sudoku pair values 
        print("Sudoku 1")
        for i,z in enumerate(final_ans):
            if( z< 10):  print(z, end="   ")
            if ( z>=10 ): print(z,end="  ")
            if( (i+1)%M == 0): print(" ",end=" ")
            if (i+1)%N==0: print('\n')
            if( i+1 == N*N ): print("Sudoku 2 \n")

    # Else printing Not valid
    else: print("Not Valid")
end = time.time()
print(end -start)
   
   



