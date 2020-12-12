from ortools.linear_solver import pywraplp


def mip_solver(sets, item_count, start_solution, max_time):
    if len(sets) > 2000000:
        print("Too many sets for MIP-Solver: ",len(sets))
        return start_solution, 0

    solution = start_solution
    cover = [0]*len(sets)
    for s in sets:
        cover[s.index] = [0]*item_count
        for item in s.items:
            cover[s.index][item] = 1

    solver = pywraplp.Solver.CreateSolver(solver_id='SCIP')
    x = [solver.IntVar(0, 1, 'x'+str(s.index)) for s in sets]
    for j in range(item_count):
        solver.Add(solver.Sum([x[s.index]*cover[s.index][j] for s in sets]) >= 1)
    
    solver.Minimize(solver.Sum([x[s.index]*s.cost for s in sets]))
    solver.SetTimeLimit(int(max_time*1000))
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print('Total cost = ', solver.Objective().Value(), '\n')
        for s in sets:
            solution[s.index] = int(x[s.index].solution_value())
    else:
        print("submitting greedy solution")
    return solution, int(status == pywraplp.Solver.OPTIMAL)
