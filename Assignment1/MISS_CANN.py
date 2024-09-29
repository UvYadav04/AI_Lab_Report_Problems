from collections import deque

def isValid(state):
    missionaries, cannibals, boat = state
    if missionaries < 0 or cannibals < 0 or missionaries > 3 or cannibals > 3:
        return False
    if missionaries > 0 and missionaries < cannibals:
        return False
    if 3 - missionaries > 0 and 3 - missionaries < 3 - cannibals:
        return False
    return True

def getSuccessors(state):
    successors = []
    missionaries, cannibals, boat = state
    moves = [(2, 0), (0, 2), (1, 1), (1, 0), (0, 1)]
    if boat == 1:
        for move in moves:
            newState = (missionaries - move[0], cannibals - move[1], 0)
            if isValid(newState):
                successors.append(newState)
    else:
        for move in moves:
            newState = (missionaries + move[0], cannibals + move[1], 1)
            if isValid(newState):
                successors.append(newState)
    return successors

def bfs(startState, goalState):
    stateQueue = deque([(startState, [])])
    visitedStates = set()
    while stateQueue:
        state, path = stateQueue.popleft()
        if state in visitedStates:
            continue
        visitedStates.add(state)
        path = path + [state]
        if state == goalState:
            return path
        for successor in getSuccessors(state):
            stateQueue.append((successor, path))
    return None

startState = (3, 3, 1)
goalState = (0, 0, 0)

solution = bfs(startState, goalState)
if solution:
    print("Solution found:")
    for step in solution:
        print(step)
else:
    print("No solution found.")
