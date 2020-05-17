
import random

class Game:
  def __init__(self, size):
    self.board = []
    self.size = size
    self.turn = 'X'
    self.moves = 0

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


  def staticEvaluation(self, x, y):
    # Counts the score for the position.
    # if x == 2 and y == 2:
    #   return -5
    # if player == 'X':
    #   return random.randint(-5,5)
    # return 0
    return random.randrange(-5, 6)

  def minimax(self, x, y, depth, alpha, beta, player):
    if (depth == 0 or self.moves == self.size*self.size): # Or game over
      return self.staticEvaluation(x, y)
    
    if player == 'X':
      maxEval = -999
      for i in range(self.size):
        for j in range(self.size):
          if (self.board[i][j] == ' '):
            self.moves = self.moves + 1
            self.board[i][j] = 'X'
            value = self.minimax(i, j, depth - 1, alpha, beta, 'O')
            print(value)
            self.board[i][j] = ' '
            self.moves = self.moves - 1
            maxEval = max(maxEval, value)
            alpha = max(alpha, value)
            if beta <= alpha:
              # print("Pruning X")
              break
      
      return maxEval
            
    else: 
      minEval = 999
      for i in range(self.size):
        for j in range(self.size):
          if (self.board[i][j] == ' '):
            self.board[i][j] = 'O'
            self.moves = self.moves + 1
            value = self.minimax(i, j, depth - 1, alpha, beta, 'X')
            print(value)
            self.board[i][j] = ' '
            self.moves = self.moves - 1
            minEval = min(minEval, value)
            beta = min(beta, value)
            if beta <= alpha:
              # print("Pruning O")
              break
      
      return minEval


    # Undo any changes on board.
    return 0

  def doBestMove(self):
    if (self.turn == 'X'):
      # valueboard = self.board.copy()
      bestI = 0
      bestJ = 0
      maxValue = -999
      for i in range(self.size):
        for j in range(self.size):
          # Replace 0, 0 with alpha-beta values
          if self.board[i][j] == ' ':
            newMax = max(maxValue, self.minimax(i, j, 3, -999, 999, self.turn)) 
            # print("Newmax: " + str(newMax))
            # print("maxValue: " + str(maxValue))
            if (newMax > maxValue):
              bestI = i
              bestJ = j
              maxValue = newMax
      
      print("Placing X in position " + str(bestI) + ":" + str(bestJ))
      self.board[bestI][bestJ] = "X"
      self.turn = 'O'
      self.moves = self.moves + 1
        
    elif (self.turn == "O"):
      bestI = 0
      bestJ = 0
      minValue = 999
      for i in range(self.size):
        for j in range(self.size):
          # Replace 0, 0 with alpha-beta values
          if self.board[i][j] == ' ':
            newMin = min(minValue, self.minimax(i, j, 3, -999, 999, self.turn)) 
            if (newMin < minValue):
              bestI = i
              bestJ = j
              minValue = newMin
      
      print("Placing O in position " + str(bestI) + ":" + str(bestJ))
      self.board[bestI][bestJ] = "O"
      self.turn = 'X'
      self.moves = self.moves + 1

  def botPlay(self):
    for _ in range(4):
      self.doBestMove()
    
    self.printBoard()


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



game = Game(2)
game.printBoard()

game.botPlay()
# game.playGame()












