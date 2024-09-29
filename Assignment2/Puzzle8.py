import random

class PuzzleGame:
    
    def moveTile(self, dir):
        row, col = self.findEmptyTile()
        if dir == 'up' and row > 0:
            self.board[row][col], self.board[row - 1][col] = self.board[row - 1][col], self.board[row][col]
        elif dir == 'down' and row < 2:
            self.board[row][col], self.board[row + 1][col] = self.board[row + 1][col], self.board[row][col]
        elif dir == 'left' and col > 0:
            self.board[row][col], self.board[row][col - 1] = self.board[row][col - 1], self.board[row][col]
        elif dir == 'right' and col < 2:
            self.board[row][col], self.board[row][col + 1] = self.board[row][col + 1], self.board[row][col]

    def isSolved(self):
        return self.board == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    def init(self):
        self.board = self.createRandomBoard()
        self.emptyTilePos = (2, 2)

    def findEmptyTile(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return (i, j)

    def display(self):
        for row in self.board:
            print(' '.join(str(num) if num != 0 else ' ' for num in row))

    def createRandomBoard(self):
        numbers = list(range(1, 9)) + [0]
        random.shuffle(numbers)
        return [numbers[i:i + 3] for i in range(0, 9, 3)]

    def resetBoard(self):
        self.board = self.createRandomBoard()
        self.emptyTilePos = self.findEmptyTile()

if __name__ == "__main__":
    puzzle = PuzzleGame()
    puzzle.display()
    while not puzzle.isSolved():
        userMove = input("Enter move (up, down, left, right): ")
        puzzle.moveTile(userMove)
        puzzle.display()
    print("Puzzle solved!")
