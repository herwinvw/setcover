from bb_solver import get_cost
CP_SOLUTION_LIMIT = float("inf")
from ortools.sat.python import cp_model

def cp_solver(sets, item_count, start_solution, start_cost, max_time):
    if len(sets) > CP_SOLUTION_LIMIT:
        print("Too many sets for MIP-Solver: ",len(sets))
        return start_solution, 0
    model = cp_model.CpModel()
    
    solution = start_solution
    cover = [0]*len(sets)
    for s in sets:
        cover[s.index] = [0]*item_count
        for item in s.items:
            cover[s.index][item] = 1

    x = [model.NewIntVar(0, 1, 'x'+str(s.index)) for s in sets]
    for j in range(item_count):
        model.Add(sum([x[s.index]*cover[s.index][j] for s in sets]) >= 1)
    
    #cost = model.NewIntVar(0, start_cost, 'costs')
    #model.Add(cost == sum([x[s.index]*s.cost for s in sets]))
    model.Minimize(sum([x[s.index]*int(s.cost) for s in sets]))
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = max_time
    #solver.parameters.log_search_progress = True
    #solver.parameters.num_search_workers = 4
    status = solver.Solve(model)
    
    if (status == cp_model.OPTIMAL) | (status == cp_model.FEASIBLE):        
        print('Total cost = ', solver.Objective().Value(), '\n')
        for s in sets:
            solution[s.index] = int(x[s.index].solution_value())
    else:
        print("submitting greedy solution")
    return solution, int(status == cp_model.OPTIMAL)