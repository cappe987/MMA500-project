



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

  def getDiagonals(self, x, y):
    # ls = [(x-2, y-1), (x-2, y+1), (x+2, y-1), (x+2, y+1)]
    ls = [(x-1, y-2), (x-2, y-1), (x-1,y+1), (x+1, y+2), (x+2, y+1), (x+1, y-1)]
    newls = []
    for (i,j) in ls:
      if i >= 0 and i < self.size and j >= 0 and j < self.size:
        newls.append((i,j))
    
    return newls

  def findPathLength(self, player, path):
    if player == 'X':
      # Left -> Right
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
    for xs in paths_to_use: #self.mergePaths(x,y, paths_to_use):
      length = self.findPathLength(player, xs)
      if length > maxlen:
        maxlen = length

    return maxlen #if player == "X" else -maxlen

  def staticEvaluation(self, player, x_paths, o_paths):
    if (player == 'X'):
      # valueboard = self.board.copy()
      print("X:")
      print(x_paths)
      bestI = 0
      bestJ = 0
      maxValue = -999
      for i in range(self.size):
        for j in range(self.size):
          # Replace 0, 0 with alpha-beta values
          if self.board[i][j] == ' ':
            newMax = self.findMaxLength(player, self.mergePaths(i,j, x_paths), o_paths)
            if (newMax > maxValue):
              bestI = i
              bestJ = j
              maxValue = newMax
              print(newMax)
              print("BestI: " + str(bestI))
              print("BestJ: " + str(bestJ))
        
      return (bestI, bestJ, maxValue)

    elif (player == "O"):
      print("O:")
      print(o_paths)
      bestI = 0
      bestJ = 0
      maxValue = -999
      for i in range(self.size):
        for j in range(self.size):
          # Replace 0, 0 with alpha-beta values
          if self.board[i][j] == ' ':
            newMax = self.findMaxLength(player, x_paths, self.mergePaths(i,j, o_paths))
            if (newMax > maxValue):
              bestI = i
              bestJ = j
              maxValue = newMax
              print(newMax)
              print("BestI: " + str(bestI))
              print("BestJ: " + str(bestJ))
      
      return (bestI, bestJ, -maxValue) 

    # self.paths = self.mergePaths(bestI, bestJ, self.paths)

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
      # if index != index2 and (not set(paths[index]).isdisjoint(set(paths[index2]))):
      if firstConnect != index2 and (i,j) in paths[index2]:
        p = paths[index2]
        paths[firstConnect] = list(set(paths[firstConnect]).union(p))
        to_remove.append(p)

    # Remove merged paths.
    # for p in to_remove:
      # paths.remove(p)  
    paths = list(filter(lambda x: x not in to_remove, paths))

    # Nothing connected. Create its own path
    if not found:
      # paths.append([(i,j)])
      paths = [[(i,j)]] + paths
    
    return paths



  def minimax(self, depth, alpha, beta, x_paths, o_paths, player):
    if self.moves == self.size*self.size:
      # Board full, only move possible.
      # ? Think about this one
      return (-1, -1, self.findMaxLength(player, x_paths, o_paths)) 
    if (depth == 0): # Or game over
      return self.staticEvaluation(player, x_paths, o_paths)
    
    if player == 'X':
      maxEval = -999
      for i in range(self.size):
        for j in range(self.size):
          if (self.board[i][j] == ' '):
            self.moves = self.moves + 1
            self.board[i][j] = 'X'
            # Add (i,j) to paths as well
            (i2, j2, value) = self.minimax(depth - 1, alpha, beta, 
                      self.mergePaths(i,j,x_paths), o_paths, 'O')
            # print(value)
            # print("Depth: " + str(depth) + "| X: " + str(value))
            # print("Checking position: " + str(i) + " " + str(j))
            self.board[i][j] = ' '
            self.moves = self.moves - 1

            if i2 == -1 and j2 == -1:
              return (i, j, value)             

            if value > maxEval:
              maxEval = value
              bestI = i2
              bestJ = j2
              
            alpha = max(alpha, value)
            if beta <= alpha:
              # print("Pruning X")
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
            # print(value)
            # print("X: " + str(i) + " | Y: " + str(j) + " | " + str(value))
            # print("Depth: " + str(depth) + " | O: " + str(value))
            self.board[i][j] = ' '
            self.moves = self.moves - 1

            if i2 == -1 and j2 == -1:
              return (i, j, value)             

            if value < minEval:
              minEval = value
              bestI = i2
              bestJ = j2

            beta = min(beta, value)
            if beta <= alpha:
              # print("Pruning O")
              break
      
      return (bestI, bestJ, minEval)

    # Undo any changes on board.
    return 0


  def doMove(self, board, moves, turn, otherpaths):
    self.board = board
    self.moves = moves
    # self.my_turn = turn
    self.otherpaths = otherpaths

    if self.symbol == "X":
      (bestI, bestJ, _) = self.minimax(1, -999, 999, self.paths, otherpaths, "X")
    else:
      (bestI, bestJ, _) = self.minimax(1, -999, 999, otherpaths, self.paths, "O")
    
    self.paths = self.mergePaths(bestI, bestJ, self.paths)

    return (bestI, bestJ)





# Move the doMove loops into static evaluation. Static evaluation should always look at what all possible moves are and which is the best. The current static evaluation code should be placed where doMove calls minimax.


if __name__ == "__main__":
  ai = AI(10, "X")

  # xs = [[(1,1), (2,2)], [(4,4)]]
  # print(ai.mergePaths(1,2, xs)) # Merge with 1
  xs = [[(1,1), (0,0)]]
  print(ai.staticEvaluation)
  # print(ai.getNeighbours(1,3))
  # print(ai.mergePaths(3,3, [[(1,1), (2,2)], [(4,4)]])) # Merge with 2
  # print(ai.mergePaths(7,7, [[(1,1), (2,2)], [(4,4)]])) # Create new path
  # print()

  # print(ai.staticEvaluation(1,2, "X", [[(1,1), (2,2)], [(4,4)]], [])) # Merge with 1
  # print(ai.staticEvaluation(3,3, "X", [[(1,1), (2,2)], [(4,4)]], [])) # Merge with 2
  # print(ai.staticEvaluation(7,7, "X", [[(1,1), (2,2)], [(4,4)]], [])) # Create new path
  print()

  # print(ai.staticEvaluation(1,2, "O", [], [[(1,1), (2,2)], [(4,4)]])) # Merge with 1
  # print(ai.staticEvaluation(3,3, "O", [], [[(1,1), (2,2)], [(4,4)]])) # Merge with 2
  # print(ai.staticEvaluation(7,7, "O", [], [[(1,1), (2,2)], [(4,4)]])) # Create new path

  # print(ai.findPathLength("X", [(2, 2), (4, 4), (3, 3), (1, 1)]))

  # print(ai.staticEvaluation(1,2, ))