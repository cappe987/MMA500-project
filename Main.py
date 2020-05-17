
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

  def getNeighbours(self, x, y):
    ls = [(x+1,y), (x-1, y), (x, y+1), (x, y-1), (x-1, y-1), (x+1, y+1)]
    newls = []
    for (i,j) in ls:
      if i >= 0 and i < self.size and j >= 0 and j < self.size:
        newls.append((i,j))
    
    return newls

  def getDiagonals(self, x, y):
    # ls = [(x-2, y-1), (x-2, y+1), (x+2, y-1), (x+2, y+1)]
    ls = [(x-1, y-2), (x-2, y-1), (x-1,y+1), (x+1, y+2), (x+2, y+1), (x+1, y-1)]
    newls = []
    for (i,j) in ls:
      if i >= 0 and i < self.size and j >= 0 and j < self.size:
        newls.append((i,j))
    
    return newls

  def staticEvaluation(self, x, y, player):
    notPlayer = 'X' if player == 'O' else 'O'
    val = 0
    for (i,j) in self.getNeighbours(x, y):
      if self.board[i][j] == player:
        val = val + 1
      elif self.board[i][j] == notPlayer:
        val = val - 2

    return val if player == 'X' else -val
    # Counts the score for the position.
    # if x == 2 and y == 2:
    #   return -5
    # if player == 'X':
    #   return random.randint(-5,5)
    # return 0
    # return random.randrange(-5, 6)

  def minimax(self, x, y, depth, alpha, beta, player):
    if (depth == 0 or self.moves == self.size*self.size): # Or game over
      return self.staticEvaluation(x, y, player)
    
    if player == 'X':
      maxEval = -999
      for i in range(self.size):
        for j in range(self.size):
          if (self.board[i][j] == ' '):
            self.moves = self.moves + 1
            self.board[i][j] = 'X'
            value = self.minimax(i, j, depth - 1, alpha, beta, 'O')
            # print(value)
            # print("Depth: " + str(depth) + "| X: " + str(value))
            # print("Checking position: " + str(i) + " " + str(j))
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
            # print(value)
            # print("X: " + str(i) + " | Y: " + str(j) + " | " + str(value))
            # print("Depth: " + str(depth) + " | O: " + str(value))
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
            newMax = max(maxValue, self.minimax(i, j, 0, -999, 999, self.turn)) 
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
            newMin = min(minValue, self.minimax(i, j, 1, -999, 999, self.turn)) 
            if (newMin < minValue):
              bestI = i
              bestJ = j
              minValue = newMin
              print(newMin)
              print("BestI: " + str(bestI))
              print("BestJ: " + str(bestJ))
      
      print("Placing O in position " + str(bestI) + ":" + str(bestJ))
      self.board[bestI][bestJ] = "O"
      self.turn = 'X'
      self.moves = self.moves + 1

  def botPlay(self):
    for _ in range(25):
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












