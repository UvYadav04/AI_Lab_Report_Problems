from string import ascii_lowercase
import random
from itertools import combinations

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
    
    new_problems = [[list(clause) for clause in problem] for problem in problems]
    return new_problems

problems = create_problem(m, k, n)

for problem in problems:
    print(problem)
