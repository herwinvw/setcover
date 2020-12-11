# setcover
Solutions to the setcover problem of the discrete optimization course (https://www.coursera.org/learn/discrete-optimization/).

# Default solution

Add sets one-by-one until all the items are covered
Score: 18/60 points

# Greedy solution

Recursively adds the set that covers the most uncovered items for the lowest costs per item, until all items are covered.
Score: 38/60 points

## MIP specification

Minimize $\sum_i c_ix_i$
subject to
$\forall j: sum_i x_i cover_{i,j} >= 1$
