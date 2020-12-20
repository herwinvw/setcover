import time
from greedy_solver import greedy_solver


def _is_valid(sets, current_taken, covered, item_count):
    cov = covered.copy()
    for s in sets[len(current_taken):len(sets)]:
        cov |= s.items
        if len(cov)==item_count:
            return True
    return False


def _back_track(sets, current_taken, item_count):
    last_branch = None
    for i, t in reversed(list(enumerate(current_taken))):
        if t == 1:
            last_branch = i
            break

    if last_branch is None:
        return None, None

    new_taken = current_taken[0:last_branch+1]
    new_taken[last_branch] = 0

    covered = get_covered(sets, new_taken)
    if not _is_valid(sets, new_taken, covered, item_count):
        new_taken, covered = _back_track(sets, new_taken, item_count)
    return new_taken, covered


def get_covered(sets, current_taken):
    covered = set()
    for i, t in enumerate(current_taken):
        if t:
            covered |= sets[i].items
    return covered


def get_cost(sets, current_taken):
    return sum([sets[i].cost*t for i, t in enumerate(current_taken)])

def opt_heuristic(remaining_sets, covered, item_count):
    sorted_sets = sorted(remaining_sets, key=lambda s: len(s.items - covered)/s.cost, reverse=True)
    
    num_covered = len(covered)
    cost = 0
    for s in sorted_sets:
        s_covered = len(s.items - covered)
        remaining = item_count-num_covered
        if remaining == 0:
            break        
        if s_covered < remaining:
            num_covered += s_covered
            cost += s.cost
        else:
            cost += (s.cost*remaining)/s_covered
            break        
        
    return cost


def _bb_solve(sets, item_count, best_taken, best_cost, max_time):
    covered = set()
    start = time.time()
    optimal = 0
    current_taken = []
    current_cost = 0
    num_iterations = 0
    while (not max_time) or (time.time()-start) < max_time:
        backtrack = False

        # covered everything?
        if len(covered) == item_count:
            backtrack = True
            if current_cost < best_cost:
                best_cost = current_cost
                best_taken = current_taken

        # every path on the branch leads to > best_value => backtrack
        min_cost = current_cost + \
            opt_heuristic(sets[len(current_taken):len(sets)],
                          covered, item_count)
        
        if min_cost > best_cost:
            backtrack = True

        if backtrack:
            current_taken, covered = _back_track(sets, current_taken, item_count)
            if current_taken is None:
                optimal = 1
                break
            else:
                current_cost = get_cost(sets, current_taken)
        else:
            s = sets[len(current_taken)]
            covered |= s.items
            current_cost += s.cost
            current_taken.append(1)            
        num_iterations += 1
    progress = sum([s * pow(2, (len(sets)-i)) for i,s in enumerate(current_taken)])
    return best_taken, optimal, num_iterations, progress


def bb_solver(sets, item_count, max_time=None):
    sorted_sets = sorted(sets, key=lambda s: s.cost/len(s.items))
    #sorted_sets = sorted(sets, key=lambda s: len(s.items), reverse=True)
    best_taken = greedy_solver(sorted_sets, item_count)
    best_cost = get_cost(sorted_sets, best_taken)
    sorted_best_taken = [0]*len(sets)
    for i, s in enumerate(sorted_sets):
        sorted_best_taken[i] = best_taken[s.index]
        
    sorted_taken, optimal, num_iterations, progress = _bb_solve(sorted_sets, item_count, sorted_best_taken, best_cost, max_time)
    taken = [0]*len(sets)
    for i,t in enumerate(sorted_taken):
        taken[sorted_sets[i].index] = t

    return taken, optimal, num_iterations, progress