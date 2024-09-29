import numpy as np
import matplotlib.pyplot as plt
from itertools import product
from collections import deque
from time import time
from datetime import timedelta

startTime = time()

LEFT = 1
RIGHT = 2
UP = 3
DOWN = 4

moveNames = {LEFT: 'LEFT', RIGHT: 'RIGHT', UP: 'UP', DOWN: 'DOWN'}
moveDirs = {LEFT: (-1, 0), RIGHT: (1, 0), UP: (0, 1), DOWN: (0, -1)}

boardTemplate = np.matrix((
    (0, 0, 1, 1, 1, 0, 0),
    (0, 0, 1, 1, 1, 0, 0),
    (1, 1, 1, 1, 1, 1, 1),
    (1, 1, 1, 1, 1, 1, 1),
    (1, 1, 1, 1, 1, 1, 1),
    (0, 0, 1, 1, 1, 0, 0),
    (0, 0, 1, 1, 1, 0, 0)
), dtype=np.bool_)

newBoard = np.matrix((
    (0, 0, 1, 1, 1, 0, 0),
    (0, 0, 1, 1, 1, 0, 0),
    (1, 1, 1, 1, 1, 1, 1),
    (1, 1, 1, 0, 1, 1, 1),
    (1, 1, 1, 1, 1, 1, 1),
    (0, 0, 1, 1, 1, 0, 0),
    (0, 0, 1, 1, 1, 0, 0)
), dtype=np.bool_)

winningBoard = np.matrix((
    (0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 1, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0)
), dtype=np.bool_)

winningMoves = (
    (5, 3, 1), (4, 5, 4), (6, 4, 1), (6, 2, 3), (4, 3, 3), (4, 6, 4), (4, 2, 2), (4, 0, 3),
    (3, 4, 2), (6, 4, 1), (3, 6, 4), (3, 4, 2), (3, 2, 2), (6, 2, 1), (3, 0, 3), (3, 2, 2),
    (1, 4, 2), (2, 6, 4), (2, 4, 2), (5, 4, 1), (3, 4, 4), (2, 2, 2), (5, 2, 1), (2, 0, 3),
    (2, 3, 4), (0, 2, 2), (3, 2, 1), (0, 4, 4), (0, 2, 2), (2, 1, 3), (1, 3, 2)
)


class MarbleGame:
    
    def _showMove(self, move):
        r, c, direction = move
        self.ax.arrow(r, c, 2 * moveDirs[direction][0], 2 * moveDirs[direction][1], width=.01, color='b')
    
    def _applyMoveSet(self, boardState, moveSet):
        for move in moveSet:
            self._move(boardState, move)

    def _printMoves(self, boardState):
        moves = self._getLegalMoves(boardState)
        for move in moves:
            print(f'({move[0]}, {move[1]}) {moveNames[move[2]]}')
    
    def _showBoard(self, boardState):
        self.ax.clear()
        self.ax.scatter(*np.where(boardTemplate & ~boardState), s=400, facecolors='none', edgecolors='r')
        self.ax.scatter(*np.where(boardTemplate & boardState), s=400, facecolors='r', edgecolors='r')
        plt.show(block=False)

    def _getLegalMoves(self, boardState):
        moves = []
        for r, c in product(range(boardTemplate.shape[0]), range(boardTemplate.shape[1])):
            if boardState[r, c]:
                moves.extend(self._getPieceMoves(boardState, r, c))
        return moves

    def _move(self, boardState, move):
        r, c, direction = move
        boardState[r, c] = False
        boardState[r + moveDirs[direction][0], c + moveDirs[direction][1]] = False
        boardState[r + 2 * moveDirs[direction][0], c + 2 * moveDirs[direction][1]] = True
    
    def _depthFirstSearch(self, initialBoard=newBoard, finalBoard=winningBoard):
        potentialMoveSets = deque([[]])
        for i in range(10000000):
            moveSet = potentialMoveSets.pop()
            boardState = np.copy(initialBoard)
            self._applyMoveSet(boardState, moveSet)

            if np.equal(boardState, winningBoard).all():
                print('-DONE-')
                print(moveSet)
                print()
                return moveSet
            
            for move in self._getLegalMoves(boardState):
                potentialMoveSets.append(moveSet + [move])

            if (i % 50000 == 0):
                print('------')
                print('\t', 'Iteration:   ', i)
                print('\t', 'Runtime:     ', timedelta(seconds=time() - startTime))
                print('\t', 'Queue size:  ', len(potentialMoveSets))
                print()
    
    def _getPieceMoves(self, boardState, r, c):
        moves = []
        if (c >= 2):
            if boardState[r, c - 1] & boardTemplate[r, c - 2] & ~boardState[r, c - 2]:
                moves.append((r, c, DOWN))
        if (c <= boardTemplate.shape[1] - 3):
            if boardState[r, c + 1] & boardTemplate[r, c + 2] & ~boardState[r, c + 2]:
                moves.append((r, c, UP))
        if (r <= boardTemplate.shape[0] - 3):
            if boardState[r + 1, c] & boardTemplate[r + 2, c] & ~boardState[r + 2, c]:
                moves.append((r, c, RIGHT))
        if (r >= 2):
            if boardState[r - 1, c] & boardTemplate[r - 2, c] & ~boardState[r - 2, c]:
                moves.append((r, c, LEFT))
        return moves
    
    def _simulateMoves(self, boardState, moveSet):
        self._showBoard(boardState)
        for move in moveSet:
            if (input('Next? ') != ''): return
            self._move(boardState, move)
            self._showBoard(boardState)
            self._showMove(move)
        input('Done? ')
    
    def simulateMoves(self, moveSet):
        return self._simulateMoves(self.boardState, moveSet)
    
    def printMoves(self):
        return self._printMoves(self.boardState)
    
    def depthFirstSearch(self):
        return self._depthFirstSearch()
    
    def showBoard(self):
        return self._showBoard(self.boardState)

    def __init__(self, initialBoard=newBoard):
        self.boardState = np.matrix(initialBoard)
        self.fig, self.ax = plt.subplots(dpi=100, facecolor='w')
        plt.axis('off')


if __name__ == '__main__':
    game = MarbleGame()

    moveSet = game.depthFirstSearch()
    game.simulateMoves(moveSet)
