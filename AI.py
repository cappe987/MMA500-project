



class AI:

  def __init__(self, size, symbol):
    self.size = size
    self.paths = []
    self.symbol = symbol

  def getNeighbours(self, x, y):
    ls = [(x+1,y), (x-1, y), (x, y+1), (x, y-1), (x-1, y-1), (x+1, y+1)]
    newls = []
    for (i,j) in ls:
      if i >= 0 and i < self.size and j >= 0 and j < self.size:
        newls.append((i,j))
    
    return newls

  def findPathLength(self, player, path):
    if player == 'X':
      # X: Left -> Right
      lowest = 999
      highest = -1
      for (_,j) in path:
        if j < lowest:
          lowest = j
        if j > highest:
          highest = j

      return highest - lowest + 1

    else: 
      # O: Up -> Down
      lowest = 999
      highest = -1
      for (i,_) in path:
        if i < lowest:
          lowest = i
        if i > highest:
          highest = i

      return highest - lowest + 1

  def findMaxLength(self, player, x_paths, o_paths):
    paths_to_use = x_paths if player == "X" else o_paths

    maxlen = 0
    for xs in paths_to_use: 
      length = self.findPathLength(player, xs)
      if length > maxlen:
        maxlen = length

    return maxlen 

  def staticEvaluation(self, player, x_paths, o_paths):
    if (player == 'X'):
      bestI = 0
      bestJ = 0
      maxValue = -999

      # Find best move for X
      for i in range(self.size):
        for j in range(self.size):
          if self.board[i][j] == ' ':
            newMax = self.findMaxLength(player, self.mergePaths(i,j, x_paths), o_paths)
            if (newMax > maxValue):
              bestI = i
              bestJ = j
              maxValue = newMax
        
      return (bestI, bestJ, maxValue)

    elif (player == "O"):
      bestI = 0
      bestJ = 0
      maxValue = -999
      # Find best move for O
      for i in range(self.size):
        for j in range(self.size):
          # Replace 0, 0 with alpha-beta values
          if self.board[i][j] == ' ':
            newMax = self.findMaxLength(player, x_paths, self.mergePaths(i,j, o_paths))
            if (newMax > maxValue):
              bestI = i
              bestJ = j
              maxValue = newMax

      
      return (bestI, bestJ, -maxValue) 


  def mergePaths(self, i, j, path_orig):
    paths = path_orig[:]
    neighbours = self.getNeighbours(i, j)
    # print(neighbours)
    found = False
    firstConnect = -1
    for index in range(len(paths)):
      for n in neighbours:
        if n in paths[index]:
          # Connected path found
          paths[index] = [(i,j)] + paths[index]
          if not found:
            firstConnect = index
          found = True
          break

    
    # Merge paths
    to_remove = []
    for index2 in range(len(paths)):
      if firstConnect != index2 and (i,j) in paths[index2]:
        p = paths[index2]
        paths[firstConnect] = list(set(paths[firstConnect]).union(p))
        to_remove.append(p)

    # Remove merged paths.
    paths = list(filter(lambda x: x not in to_remove, paths))

    # Nothing connected. Create its own path
    if not found:
      paths = [[(i,j)]] + paths
    
    return paths



  def minimax(self, depth, alpha, beta, x_paths, o_paths, player):
    if self.moves == self.size*self.size:
      # Board full.
      # ? Think about this one
      return (-1, -1, self.findMaxLength(player, x_paths, o_paths)) 
    if (depth == 0): 
      return self.staticEvaluation(player, x_paths, o_paths)
    
    if player == 'X':
      maxEval = -999
      for i in range(self.size):
        for j in range(self.size):
          if (self.board[i][j] == ' '):
            self.moves = self.moves + 1
            self.board[i][j] = 'X'

            (i2, j2, value) = self.minimax(depth - 1, alpha, beta, 
                      self.mergePaths(i,j,x_paths), o_paths, 'O')

            self.board[i][j] = ' '
            self.moves = self.moves - 1

            if i2 == -1 and j2 == -1:
              return (i, j, value)             

            if value > maxEval:
              maxEval = value
              bestI = i
              bestJ = j
              
            alpha = max(alpha, value)
            if beta <= alpha:
              break
      
      return (bestI, bestJ, maxEval)
            
    else: 
      minEval = 999
      for i in range(self.size):
        for j in range(self.size):
          if (self.board[i][j] == ' '):
            self.board[i][j] = 'O'
            self.moves = self.moves + 1
            (i2, j2, value) = self.minimax(depth - 1, alpha, beta,
                      x_paths, self.mergePaths(i,j, o_paths), 'X')

            self.board[i][j] = ' '
            self.moves = self.moves - 1

            if i2 == -1 and j2 == -1:
              return (i, j, value)             

            if value < minEval:
              minEval = value
              bestI = i
              bestJ = j

            beta = min(beta, value)
            if beta <= alpha:
              break
      
      return (bestI, bestJ, minEval)

    # Undo any changes on board.
    return 0


  def doMove(self, board, moves, turn, otherpaths):
    self.board = board
    self.moves = moves
    # self.my_turn = turn
    self.otherpaths = otherpaths

    x_depth = 3
    o_depth = 2

    if self.symbol == "X":
      (bestI, bestJ, _) = self.minimax(x_depth, -999, 999, self.paths, otherpaths, "X")
    else:
      (bestI, bestJ, _) = self.minimax(o_depth, -999, 999, otherpaths, self.paths, "O")
    
    self.paths = self.mergePaths(bestI, bestJ, self.paths)

    return (bestI, bestJ)





# Move the doMove loops into static evaluation. Static evaluation should always look at what all possible moves are and which is the best. The current static evaluation code should be placed where doMove calls minimax.


if __name__ == "__main__":
  ai = AI(10, "X")
