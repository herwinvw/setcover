# setcover
Solutions to the setcover problem of the discrete optimization course (https://www.coursera.org/learn/discrete-optimization/).

# Default solution

Add sets one-by-one until all the items are covered
Score: 18/60 points

# Greedy solution

Recursively adds the set that covers the most uncovered items for the lowest costs per item, until all items are covered.
Score: 38/60 points

# Branch and bound solution
Every branch encodes whether or not to take a set. Takes the costs of the greedy solution as first solution for best costs.

The decision tree can be pruned when:
* Taking a set does not increase the cover
* Current cost + lower bound remaining costs > best costs so far

The following heuristic is used to determine the lower bound of the remaining for a branch:
Given N items that need to be covered. 
1. remaining_cost = 0
2. From the remaining sets, find the set s that has lowest cost per yet uncovered item
3. If uncovered items in s > N then remaining_cost+= N*(cost of s / uncovered items in s)
4. Else remaining_cost+=costs of s, N-=uncovered items in s, goto 2

Score: 38/60 points

# MIP solution

Minimize sum_i(c[i] x[i])
subject to
forall j: sum_i x[i] cover[i,j] >= 1

With cover[i,j] in {0,1}, indicating that set i covers j.

Score: 60/60

# CP solution
Using the same formulation as the MIP solution

Score: 41/60
