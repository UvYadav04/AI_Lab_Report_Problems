def dfs(startState, goalState):
    stateStack = [(startState, [])]
    visitedStates = set()

    while stateStack:
        currentState, path = stateStack.pop()

        if currentState == goalState:
            return path + [currentState]

        if currentState not in visitedStates:
            visitedStates.add(currentState)
            emptyIdx = currentState.index('_')
            moveOffsets = [-1, 1, -2, 2]

            for offset in moveOffsets:
                newIdx = emptyIdx + offset
                if 0 <= newIdx < len(currentState):
                    newState = list(currentState)
                    newState[emptyIdx], newState[newIdx] = newState[newIdx], newState[emptyIdx]
                    successorState = tuple(newState)
                    if successorState not in visitedStates:
                        stateStack.append((successorState, path + [currentState]))

    return None

startState = ('l', 'l', 'l', '_', 'r', 'r', 'r')
goalState = ('r', 'r', 'r', '_', 'l', 'l', 'l')

solutionDfs = dfs(startState, goalState)

print("DFS Solution:")
for step in solutionDfs:
    print(step)
