
from AI import AI
import random
import enum

class PlayerType(enum.Enum):
  Human = True
  AI = False

class Game:
  def __init__(self, size, p1, p2):
    self.board = []
    self.size = size
    self.turn = 'X'
    self.moves = 0
    self.p1 = p1
    self.p2 = p2

    self.AI1 = AI(size, "X")
    self.AI2 = AI(size, "O")

    for i in range(size):
      self.board.append([])
      for _ in range(size):
        self.board[i].append(' ')

  def printBoard(self):
    num = self.size
    for i in range(self.size):
      print(" ", end="")
    for i in range(self.size):
      print("/\\", end="")
    print()

    for i in range(self.size):
      num = num - 1
      for _ in range(num):
        print(" ", end="")

      print("|", end="")
      for j in range(self.size):
        print(str(self.board[i][j]) + "|", end="")
      print()

      for _ in range(num):
        print(" ", end="")
      print("/", end="")
      for _ in range(self.size):
        print("\\/", end="")
      print()
      # print("\n---------------")

  
#   /\
#  |5 |
#   \/

  def doBestMove(self):
    if (self.turn == 'X'):
      (bestI, bestJ) = self.AI1.doMove(self.board, self.moves, self.turn, self.AI2.paths)
      
      print("Placing X in position " + str(bestI) + ":" + str(bestJ))
      self.board[bestI][bestJ] = "X"
      self.turn = 'O'
      self.moves = self.moves + 1
        
    elif (self.turn == "O"):
      (bestI, bestJ) = self.AI2.doMove(self.board, self.moves, self.turn, self.AI1.paths)
      
      print("Placing O in position " + str(bestI) + ":" + str(bestJ))
      self.board[bestI][bestJ] = "O"
      self.turn = 'X'
      self.moves = self.moves + 1

  def playGame(self):
    while self.moves != self.size*self.size:
      if self.turn == 'X':
        if self.p1 == PlayerType.Human:
          self.humanInput()
        else:
          self.doBestMove()
      else:
        if self.p2 == PlayerType.Human:
          self.humanInput()
        else:
          self.doBestMove()
      self.printBoard()



  def botPlay(self):
    for _ in range(self.size*self.size):
    # while True:
      self.doBestMove()
      self.printBoard()
      input("Press enter to continue")


  def humanInput(self):
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



game = Game(7, PlayerType.Human, PlayerType.AI)

game.printBoard()

# game.playGame()
game.botPlay()


# Keep track of paths for humans. 
# Human play currently does not work and the PlayerType isn't used.












