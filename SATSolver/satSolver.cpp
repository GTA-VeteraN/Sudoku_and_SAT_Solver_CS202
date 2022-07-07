// including the libraries
#include<bits/stdc++.h>
#include <algorithm>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <string>
#include <vector>
using namespace std;

// any function returning 0 means satisfied , 1 means unsatisfied, 2 means normal and 3 means completed

// function that applies the transform i.e, removes the entire clause or just a clause member depending upon the condition
int apply_transform(vector<int>&literals ,vector< vector<int> > &clauses , int literal_to_apply){
	int value_to_apply = literals[literal_to_apply]; // the value to be applied , 0 -true  and 1 -false
	// Iteration over the clauses
	for ( int i=0; i<(int)clauses.size() ; ++i){

		for( int j=0 ; j<(int)clauses[i].size(); ++j){

			// if literal appears with the same polarity as it is being applied
			if( (2*literal_to_apply + value_to_apply) == clauses[i][j]){
				clauses.erase(clauses.begin()+i); // erasing the entire clause
				i--;
				if( clauses.size() ==0 ) return 0; // if no clause remains then satisfiable
				break;
			}
			// if the literal appears with opposite polarity as it is being applied
			else if( clauses[i][j]/2 == literal_to_apply){
				clauses[i].erase( clauses[i].begin()+j); // erasing the literal only from the clause
				j--;
				if (clauses[i].size() == 0) return 1; // if that particular clause becomes empty, then that particular branch is unsat.
				break;
			}
		}

	}
	return 2; // function exiting normally
}

// function performing unit resolution in a formula
int unit_propogate( vector< vector<int> > &clauses , vector<int>&literals, vector<int> &literal_frequency){
	bool unit_clause_found = false; // unit clause not found
	if( clauses.size() ==0 ) return 0; // if formula has no clauses

	do{
		unit_clause_found = false;
		// iterating over the clauses
		for( int i=0 ; i<(int)clauses.size() ; ++i ){
			if( clauses[i].size() == 1){
				unit_clause_found = true; // found the unit clause
				// values assigned if the clause is positive then 0 -true , if negative then 1-false
				literals[clauses[i][0]/2] = clauses[i][0]%2; 
				literal_frequency[clauses[i][0]/2] = -1;// assigning closed
				// applying this transform to the whole set of clauses.
				int result = apply_transform(literals,clauses,clauses[i][0]/2);
				// if we get unsat ot sat then return the result.
				if( result == 0 || result == 1) return result; 
				break; // exit the loop to check for another unit clause from the start
			}
			else if( clauses[i].size() == 0) return 1;
		}
	}
	while( unit_clause_found);
	return 2; // normal return
}
// function for showing the result 
void show_result(vector<int> literals ,int result){
	if(result == 0){ // if SAT
		cout << "SAT" << "\n";
		for( int i=0 ; i< (int)literals.size() ; ++i){
			if(i!=0) cout <<" ";
			if( literals[i] != -1) cout << pow(-1 , literals[i])*(i+1);
			else cout << i+1; // if we have not assigned the values of some literals, then assign them positive values.
		}
		cout << " 0";
	}
	else cout << "UNSAT";
}
// function to perform recursive DPLL on a given formula
int DPLL(vector< vector<int> > &clauses , vector<int>&literals, vector<int> &literal_frequency, vector<int> &literal_polarity){
	// performing fisrtly unit propogation
	int result = unit_propogate(clauses, literals, literal_frequency);
	// if satisfiable
	if( result== 0) {
		show_result(literals , result);
		return 3; // return completed
	}
	// if formula not satisfied in this branch, return normally
	else if( result == 1) return 2;
	// finding literal with maximum frequency, which will be assigned the value
	int i= distance( literal_frequency.begin() , max_element(literal_frequency.begin(), literal_frequency.end()));
	// two values can be applied to the literal
	for( int j=0 ; j<2 ; ++j){
		//creating a new set of values to apply for recursion
		vector< vector<int>> new_clauses(clauses);
		vector<int> new_literals(literals);
		vector<int> new_literal_frequency(literal_frequency);
		vector<int> new_literal_polarity(literal_polarity);
		// if number of literals with positive values are more, assign positive first
		if( new_literal_polarity[i]>0) new_literals[i] = j;
		else new_literals[i] = (j+1)%2; // if not ,assign neagtive first
		new_literal_frequency[i] = -1; // reset frequency
		// applying this transform to all the clauses
		int transform_result = apply_transform(new_literals,new_clauses,i);
		// if we get staisfiable
		if( transform_result == 0 ){
			show_result(new_literals,transform_result);//show result
			return 3;
		}
		// if unsatisfiable, try another value of the literal
		else if( transform_result == 1) continue;
		// recursively call the DPLL on the new formula
		int dpll_result = DPLL(new_clauses , new_literals , new_literal_frequency , new_literal_polarity);
		if( dpll_result == 3 ) return dpll_result; // if completed , propogate the result
	}
	return 2; // returned normally 
}
void solve( vector< vector<int> > &clauses , vector<int>&literals, vector<int> &literal_frequency, vector<int> literal_polarity ){
	// final result of the DPLL on the original formula
	int result = DPLL(clauses, literals , literal_frequency , literal_polarity);
	// if we get normal return , that means no branch has satisfied the formula
	//  so we get unsatisfiable
	if( result == 2 ) show_result(literals , 1);// literal is dummy vector
}


int main(){ // 0-satisfied , 1-unsat , 2 -normal, 3-completed
	
	//Taking Input

	vector<int> literals; // storing the value assigned to each literal
	vector<int> literal_frequency; // number of occurence of any literal
	vector<int> literal_polarity; // difference in positive and negative occurence of literals
	vector< vector <int> > clauses; // stroing the clauses
	int literal_count; // number of literals
	int clause_count; // number of clauses
	char c ;
	string s;
	while(true){
		cin >> c;
		if( c == 'c') getline(cin,s); // if comment,then ignore
		else{	// we get 'p'
			cin >> s; // we get 'cnf'
			break;
		}
	}
	cin >> literal_count;
	cin >> clause_count;
	// setting the appropriate sizes to the vectors.
	literals.clear();
	literals.resize(literal_count, -1);
	clauses.clear();
	clauses.resize(clause_count);
	literal_frequency.clear();
	literal_frequency.resize(literal_count, 0);
	literal_polarity.clear();
	literal_polarity.resize(literal_count, 0);

	int literal; // store the incoming literal value
  // iterate over the clauses
  for (int i = 0; i < clause_count; i++) {
  	// while the ith clause gets more literals
    while (true) {
      cin >> literal;
      // if the variable has positive polarity
      if (literal > 0) {
       	clauses[i].push_back(2 *(literal - 1)); // store it in the form 2n
        // increment frequency and polarity of the literal
       	literal_frequency[literal - 1]++;
       	literal_polarity[literal - 1]++;
      } 
      // if the variable has negative polarity
      else if (literal < 0) {
       	clauses[i].push_back(2 * ((-1) * literal - 1) + 1); // store it in the form 2n+1
        // increment frequency and decrement polarity of the literal
       	literal_frequency[-1 - literal]++;
       	literal_polarity[-1 - literal]--;
      } 
      else {
        break; // read 0, so move to next clause
      }
    }
  }
 	// initialising the solver for the given formula.
  solve( clauses, literals , literal_frequency, literal_polarity);
  return 0;
}