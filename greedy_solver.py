def best_valued_set(sets, covered):
    max_value = 0
    sel_s = None
    for s in sets:
        uncovered = set(s.items) - covered
        value = len(uncovered)/s.cost
        if value>max_value:
            max_value = value
            sel_s = s
    return sel_s

def greedy_solver(sets, item_count):
    covered = set()
    
    solution = [0]*len(sets)
    while(len(covered) < item_count):
        s = best_valued_set(sets, covered)
        solution[s.index] = 1
        covered |= set(s.items)
        
    return solution