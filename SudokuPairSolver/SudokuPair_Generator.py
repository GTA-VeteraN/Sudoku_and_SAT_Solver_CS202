# This is the file for Sudoku Generator
# Input : You just need to enter the dimension of sudoku- k
# Output : csv file named test{random number}.csv and a message saying the name of csv file created
# along with the time of execution

# Importing important modules
import pysat
from pysat.formula import CNF 
from pysat.solvers import Cadical
import random
import csv
import time

# Taking sudoku dimension as input
M = int(input("Enter the dimension of Sudoku "))
N = M*M
start = time.time()
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
    v3 =[]
    v4 =[]
    formula = CNF()

    # Column and Row constraints for Sudoku Pair
    for i in range(N):
        for s in range(N):
           
            v1 = v1 + exactly_one([transform(i,j,s) for j in range(N)])

            
            v2 = v2 +exactly_one([transform(j,i,s) for j in range(N)])

          
            v3=  v3 +exactly_one([transform(i+N,j,s) for j in range(N)])

            
            v4 = v4 +exactly_one([transform(j,i,s) for j in range(N,2*N)])

        # For cell constraints that is exactly one value from 1 to N in each cell
        for z in v1:
            formula.append(z)
        for z in v2:
            formula.append(z)
        for z in v3:
            formula.append(z)
        for z in v4:
            formula.append(z)
        v1 = []
        v2 = []
        v3 = []
        v4 = []
        for j in range(N):
            v1 = v1 + exactly_one([transform(i,j,k) for k in range(N)])
            v2 = v2 +exactly_one([transform(i+N,j,k) for k in range(N)])

    # appending the cell constraints to the CNF formula     
    for z in v1:
        formula.append(z)
    for z in v2:
        formula.append(z)
    v1 = []
    v2 = []
    cnf =[]
    # Block Constraints, that is each MxM block should have number from 1 to N. 
    for k in range(N):
        for x in range(M):
            for y in range(M):
                v1 = [transform(y*M +i , x*M +j , k) for i in range(M) for j in range(M)] 
                v2 = [transform(y*M + N +i, x*M +j, k) for i in range(M) for j in range(M)]
                cnf = cnf + exactly_one(v1)
                cnf = cnf + exactly_one(v2)    

    for z in cnf:
        formula.append(z)

    del cnf 
    del v1
    del v2          
    # Sudoku Pair constraints that is Sudoku Pair should not have same value for same position
    for x in range(N):
        for y in range(N):
            for k in range(N):
                v1 = transform(x,y,k)
                v2 = transform(x+N, y, k)
                formula.append([-v1,-v2])

    # For making sudoku random each item we will be selecting a random place in 
    # the Sudoku pair and assign it valid random value
    constraints = [(random.randint(0, 2*N-1) ,random.randint(0,N-1) , random.randint(0, N))]
    
    # Adding the constraint to the formula
    for z in constraints:
        formula.append([transform(z[0],z[1],z[2])-1])
    solution = []
    # Solving the clauses using Cadical SAT Solver
    with Cadical( bootstrap_with=formula.clauses) as c:
        c.solve()
        solution = c.get_model()
    
    final_ans =[]
    # Extracting the solution that is positive values 
    for z in solution:
        if z>0 :
            final_ans.append(z) 
            formula.append([z])
    negation = []
    n=0
    ranger = 2*N*N -1 
    # Here We have used Naive Model Counting Method to find the maximal number of holes for 
    # a random sudoku pair. 
    # Whenever we have solution, we will simply append the negation of it to the clauses and 
    # again solve. If we get false which means we get unique solution so we remove one more value and if 
    # the value comes to be true, this implies the first case when the uniqueness of the solution got last
    # We will stop here and get the answer.
    if N<=9: 
        while(True):
            i = random.randint(0, ranger)
            v = final_ans[i]
            formula.clauses.remove([v])
            final_ans.remove(v)
            negation.append(-v)
            formula.append(negation)
            with Cadical( bootstrap_with=formula.clauses) as c:
                if c.solve(): break
            formula.clauses.pop() 
            n = n+1
            ranger = ranger-1

    # For k>=4 I tried to reduce the time taken by randomly removing some terms 
    # assuming that upto this point the sudoku will have only unique solution.
    # And after this again using Naive Model counting technique.
    else :
        # For k=4 we tested for various cases and got that every time holes more than 85
        # were there in 16x16 sudoku pair each time, so we made 80 holes without even checking 
        # for uniqueness
        if( N==16):
            while( n< 80):  # Removal of first 80 terms without checking
                i = random.randint(0, ranger)
                v = final_ans[i]
                formula.clauses.remove([v])
                final_ans.remove(v)
                negation.append(-v)
                n= n+1
                ranger = ranger-1
        # For k=5 we assumed that removing first 200 terms will always be removed and then 
        # after that we started checking for uniqueness
        elif( N==25):
            while( n< 200): # Removal of first 200 terms without checking
                i = random.randint(0, ranger)
                v = final_ans[i]
                formula.clauses.remove([v])
                final_ans.remove(v)
                negation.append(-v)
                n= n+1
                ranger = ranger-1
                # print(n)
        else:
            while( n< N*6): # Removal of first N*6 terms without checking for cases k>=6
                i = random.randint(0, ranger)
                v = final_ans[i]
                formula.clauses.remove([v])
                final_ans.remove(v)
                negation.append(-v)
                n= n+1
                ranger = ranger-1
        
        # After we removed pre-defined number of terms we again start doing Naive Model Counting
        # and checking for uniqueness
        while(True): # Removal of next terms with checking 
            i = random.randint(0, ranger)
            v = final_ans[i]
            formula.clauses.remove([v])
            final_ans.remove(v)
            negation.append(-v)
            formula.append(negation)
            with Cadical( bootstrap_with=formula.clauses) as c:
                if c.solve(): break
            formula.clauses.pop() 
            n = n+1
            ranger = ranger-1
 
    final_ans.append(-negation.pop())
    v = []
    # Transforming the variables to valid sudoku values
    for z in final_ans:
        v = v+ [inverse_transform(z)]
    v.sort()
    index=0
    # CSV preparation
    filename = "test" + str(random.randint(0,100000)) +".csv" # Filename of CSV
    field =[]
    # Adding data to the CSV file - both the holes and constraint values
    with open(filename,'w',newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for i in range(2*N):
            field_data =[]
            for j in range(N):
                if ( index < len(v)):
                    if( (v[index][0]==i)&(v[index][1]==j) ) : 
                        field_data.append(v[index][2]+1)
                        index= index+1
                    else: field_data.append(0)
                else : field_data.append(0) 
            field.append(field_data)
        
        csvwriter.writerows(field)

    # Printing the final line after execution.
    Final = "CSV file named " + filename +" successfully made."
    print(Final)
end = time.time()
print( end -start)