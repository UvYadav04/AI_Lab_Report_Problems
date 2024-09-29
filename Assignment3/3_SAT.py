from string import ascii_lowercase
from itertools import combinations
import numpy as np
import random

m = int(input("Enter the number of clauses: "))
k = int(input("Enter the number of literals in a clause: "))
n = int(input("Enter the number of variables: "))

def create_problem(m, k, n):
    pos_var = list(ascii_lowercase)[:n]
    neg_var = [v.upper() for v in pos_var]
    variables = pos_var + neg_var
    limit = 10
    problems = []
    all_combinations = list(combinations(variables, k))
    i = 0

    while i < limit:
        sample = random.sample(all_combinations, m)
        if sample not in problems:
            i += 1
            problems.append(list(sample))
    return variables, problems

variables, problems = create_problem(m, k, n)

def evaluate(problem, assignment):
    count = 0
    for clause in problem:
        z = [assignment[var] for var in clause]
        count += any(z)
    return count

def variable_neighbor(problem, assignment, step_size, step_count):
    current_assignment = assignment.copy()
    values = list(assignment.values())
    keys = list(assignment.keys())
    possible_assignments = []
    possible_scores = []
    initial_score = evaluate(problem, assignment)
    
    if initial_score == len(problem):
        return assignment, f"{step_count}/{step_count}", step_size
    
    for i in range(len(values)):
        step_count += 1
        current_assignment[keys[i]] = abs(values[i] - 1)
        score = evaluate(problem, current_assignment)
        possible_assignments.append(current_assignment.copy())
        possible_scores.append(score)
    
    selected = list(np.argsort(possible_scores))[-step_size:]
    
    if len(problem) in possible_scores:
        index = [i for i in range(len(possible_scores)) if possible_scores[i] == len(problem)][0]
        return possible_assignments[index], f"{step_count}/{step_count}", step_size
    
    for a in selected:
        return variable_neighbor(problem, a, step_size + 1, step_count)

def hill_climb(problem, assignment, parent_score, received_step, step_count):
    current_assignment = assignment.copy()
    values = list(assignment.values())
    keys = list(assignment.keys())
    max_score = parent_score
    max_assignment = assignment.copy()
    
    for i in range(len(values)):
        step_count += 1
        current_assignment[keys[i]] = abs(values[i] - 1)
        score = evaluate(problem, current_assignment)
        if score > max_score:
            received_step = step_count
            max_score = score
            max_assignment = current_assignment.copy()
    
    if max_score == parent_score:
        return assignment, max_score, f"{received_step}/{step_count-len(values)}"
    
    return hill_climb(problem, max_assignment, max_score, received_step, step_count)

def beam_search(problem, assignment, step_size, step_count):
    current_assignment = assignment.copy()
    values = list(assignment.values())
    keys = list(assignment.keys())
    possible_assignments = []
    possible_scores = []
    
    initial_score = evaluate(problem, assignment)
    
    if initial_score == len(problem):
        return assignment, f"{step_count}/{step_count}"
    
    for i in range(len(values)):
        step_count += 1
        current_assignment[keys[i]] = abs(values[i] - 1)
        score = evaluate(problem, current_assignment)
        possible_assignments.append(current_assignment.copy())
        possible_scores.append(score)
    
    selected = list(np.argsort(possible_scores))[-step_size:]
    
    if len(problem) in possible_scores:
        index = [i for i in range(len(possible_scores)) if possible_scores[i] == len(problem)][0]
        return possible_assignments[index], f"{step_count}/{step_count}"
    
    for a in selected:
        return beam_search(problem, a, step_size, step_count)

def create_assignment(variables, n):
    pos_assignment = list(np.random.choice(2, n))
    neg_assignment = [abs(1 - i) for i in pos_assignment]
    assignment = pos_assignment + neg_assignment
    return dict(zip(variables, assignment))

hill_results = []
assignments = []
hill_scores = []
initial_scores = []
hill_steps = []
beam_steps = []
var_steps = []
var_count = []
beam_vars = []
beam_scores = []
beam_assignments = []
var_assignments = []

for idx, problem in enumerate(problems):
    assignment = create_assignment(variables, n)
    initial_score = evaluate(problem, assignment)
    
    hill_result, hill_score, hill_step = hill_climb(problem, assignment, initial_score, 1, 1)
    hill_results.append(hill_result)
    assignments.append(assignment)
    hill_scores.append(hill_score)
    initial_scores.append(initial_score)
    hill_steps.append(hill_step)
    
    beam_result3, beam_step3 = beam_search(problem, assignment, 3, 1)
    beam_assignments.append(beam_result3)
    beam_steps.append(beam_step3)
    
    beam_result4, beam_step4 = beam_search(problem, assignment, 4, 1)
    
    var_result, var_step, var_size = variable_neighbor(problem, assignment, 1, 1)
    var_steps.append(var_step)
    beam_vars.append(var_size)
    var_assignments.append(var_result)
    
    print(f'Problem {idx + 1}: {problem}')
    print(f'Hill Climbing: {hill_result}, Penetration: {hill_step}')
    print(f'Beam Search (3): {beam_result3}, Penetration: {beam_step3}')
    print(f'Beam Search (4): {beam_result4}, Penetration: {beam_step4}')
    print(f'Variable Neighborhood: {var_result}, Penetration: {var_step}')
    print()
