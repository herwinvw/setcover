def best_valued_set(sets, covered):
    min_value = float('inf')
    sel_s = None
    for s in sets:
        uncovered = s.items - covered
        if len(uncovered)>0:
            cost_per_uncovered = s.cost/len(uncovered)
            if cost_per_uncovered<min_value:
                min_value = cost_per_uncovered
                sel_s = s
    return sel_s

def greedy_solver(sets, item_count):
    covered = set()
    
    solution = [0]*len(sets)
    while(len(covered) < item_count):
        s = best_valued_set(sets, covered)
        solution[s.index] = 1
        covered |= s.items
        
    return solution