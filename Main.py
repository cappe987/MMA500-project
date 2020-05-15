

class Game:
  def __init__(self, size):
    self.board = []
    self.size = size
    self.turn = 'X'

    for i in range(size):
      self.board.append([])
      for _ in range(size):
        self.board[i].append(' ')

  def printBoard(self):
    for i in range(self.size):
      for j in range(self.size):
        print(self.board[i][j], end="")
      print()

  def playGame(self):
    while(True):
      if(self.turn == 'X'):
        print("Player X")
        x = int(input("Input x: "))
        y = int(input("Input y: "))
        self.board[x][y] = "X"
        self.turn = "O"

      elif(self.turn == 'O'):
        print("Player O")
        x = int(input("Input x: "))
        y = int(input("Input y: "))
        self.board[x][y] = "O"
        self.turn = "X"

      self.printBoard()



game = Game(5)
game.printBoard()

game.playGame()


