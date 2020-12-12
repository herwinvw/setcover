import time
from greedy_solver import best_valued_set, greedy_solver


def _is_valid(sets, current_taken, item_count):
    covered = get_covered(sets, current_taken)
    for s in sets[len(current_taken):len(sets)]:
        covered |= s.items
    return len(covered) == item_count


def _back_track(sets, current_taken, item_count):
    last_branch = None
    for i, t in enumerate(current_taken):
        if t == 1:
            last_branch = i

    if last_branch is None:
        return None

    new_taken = current_taken[0:last_branch+1]
    new_taken[last_branch] = 0

    if not _is_valid(sets, new_taken, item_count):
        new_taken = _back_track(sets, new_taken, item_count)
    return new_taken


def get_covered(sets, current_taken):
    covered = set()
    for i, t in enumerate(current_taken):
        if t:
            covered |= sets[i].items
    return covered


def get_cost(sets, current_taken):
    return sum([sets[i].cost*t for i, t in enumerate(current_taken)])


def opt_heuristic(remaining_sets, covered, item_count):
    _, cost_per_item = best_valued_set(remaining_sets, covered)
    return (item_count-len(covered))*cost_per_item


def _bb_solve(sets, item_count, best_taken, best_cost, max_time):
    covered = set()
    start = time.time()
    optimal = 0
    current_taken = []
    current_cost = 0
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
            current_taken = _back_track(sets, current_taken, item_count)
            if current_taken is None:
                optimal = 1
                break
            else:
                covered = get_covered(sets, current_taken)
                current_cost = get_cost(sets, current_taken)
        else:
            s = sets[len(current_taken)]
            covered |= s.items
            current_cost += s.cost
            current_taken.append(1)

    return best_taken, optimal


def bb_solver(sets, item_count, max_time=None):
    sorted_sets = sorted(sets, key=lambda s: len(s.items)/s.cost, reverse=True)
    best_taken = greedy_solver(sorted_sets, item_count)
    best_cost = get_cost(sorted_sets, best_taken)
    sorted_taken, optimal = _bb_solve(sorted_sets, item_count, best_taken, best_cost, max_time)
    taken = [0]*len(sets)
    for i,t in enumerate(sorted_taken):
        taken[sorted_sets[i].index] = t

    return taken, optimal