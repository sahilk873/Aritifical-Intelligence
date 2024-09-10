class Strategy:

   def __init__(self):
      self.white = "o"
      self.black = "x"
      self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
      self.opposite_color = {self.black: self.white, self.white: self.black}
      self.x_max = None
      self.y_max = None
      self.logging = True

   def best_strategy(self, board, color, best_move, still_running):
    # returns best move
      self.x_max = len(board)
      self.y_max = len(board)
      if color == "#000000":
         color = "x"
      else:
         color = "o"
      searchdepth = 0
      if self.stones_left(board) > 30:
         searchdepth = 4
      if self.stones_left(board) > 15:
         searchdepth = 4
      else:
         searchdepth = 4
      move = -1
      alpha = -9999999999999999999999999999999
      beta = 999999999999999999999999999999
      v, move = self.alphabeta(board, color, searchdepth, alpha, beta, move)
      temp = [move//self.x_max,move%self.x_max]
      return temp, v

   def minimax(self, board, color, search_depth):
    # returns best "value"
      return 1
      
   def alphabeta(self, board, color, search_depth, alpha, beta, move):
      if search_depth == 0 or self.stones_left(board) == 0:
         if self.stones_left(board) == 0:
            return self.evaluate(board, color, move), move
         return self.evaluate(board, color, move), 0
      if search_depth in {0, 2, 4, 6, 8}:
         v = -999999999999999
         result = 0.1
         for move, stonesflipped in self.find_moves(board, color).items():
            mv, ms = self.alphabeta(self.make_move(board, color, move, stonesflipped), self.opposite_color[color], search_depth-1, alpha, beta, move)
            if v < mv:
               v = mv
               result = move
            if result == 0.1:
               v = mv
               result = move
            if v > beta:
               return v, result
            alpha = max(alpha, v)
         return v, result
      else:
         v = 999999999999999
         result = 0.1
         for move, stonesflipped in self.find_moves(board, color).items():
            mv, ms = self.alphabeta(self.make_move(board, color, move, stonesflipped), self.opposite_color[color], search_depth-1, alpha, beta, move)
            if v > mv:
               v = mv
               result = move
            if result == 0.1:
               v = mv
               result = move
            if v < alpha:
               return v, result
            beta = min(alpha, v)
         return v, result
         
   def stones_left(self, board):
      stonesleft = 0
      for i in range(len(board)):
         for j in range(len(board)):
            if board[i][j] == '.':
               stonesleft += 1
      return stonesleft

   def make_move(self, board, color, move, flipped):
      newboard = [r[:] for r in board]
      symbol = ''
      if color == self.black:
         symbol = 'x'
      if color == self.white:
         symbol = 'o'
      x, y = move // self.x_max, move % self.y_max
      board[x][y] == symbol
      for spots in flipped:
         newboard[spots[0]][spots[1]] = symbol
      return newboard

   def evaluate(self, board, color, move):
    # returns the utility value
      score = self.score(board, color)
      weightedtable =  [[1000,-7,2,2,2,2,-7,1000],
                        [-7,-10,-1,-1,-1,-1,-10,-7],
                        [2,-1,1,0,0,1,-1,2],
                        [2,-1,0,1,1,0,-1,2],
                        [2,-1,0,1,1,0,-1,2],
                        [2,-1,1,0,0,1,-1,2],
                        [-7,-10,-1,-1,-1,-1,-10,-7],
                        [1000, -7, 2, 2, 2, 2, -7, 1000]]
      if move != -1000000000000000000000:
         h = weightedtable[move//len(board)][move%len(board)]
         return score*h
      return score
         

   def score(self, board, color):
      mymoves = len(self.find_moves(board, color))
      oppmoves = len(self.find_moves(board, self.opposite_color[color]))
      difference = mymoves-(2*oppmoves)
      mystones = self.placedstones(board, color)
      opponentstones = self.placedstones(board, self.opposite_color[color])
      stonedifference = mystones-opponentstones
      stonesleft = self.stones_left(board)
      if stonesleft == 0:
         if mystones > opponentstones:
            return 99999999999999999
         else:
            return -99999999999999999
      if stonesleft > 35:
         hval = stonedifference * - 1
         return hval * difference
      else:
         return stonedifference * difference
      

      
   def placedstones(self, board, color):
      if color == self.black:
         symbol = 'x'
      else:
         symbol = 'o'
      counter = 0
      for i in range(len(board)):
         for j in range(len(board)):
            if board[i][j] == symbol:
               counter += 1
      return counter



   def find_flipped(self, my_board, x, y, my_color):
    if my_board[x][y] != ".":
        return []
    if my_color == self.black:
        my_color = "x"
    else:
        my_color = "o"
    flipped_stones = []
    for incr in self.directions:
        temp_flip = []
        x_pos = x + incr[0]
        y_pos = y + incr[1]
        while 0 <= x_pos < self.x_max and 0 <= y_pos < self.y_max:
            if my_board[x_pos][y_pos] == ".":
                break
            if my_board[x_pos][y_pos] == my_color:
                flipped_stones += temp_flip
                break
            temp_flip.append([x_pos, y_pos])
            x_pos += incr[0]
            y_pos += incr[1]
    return flipped_stones


   def find_moves(self, my_board, my_color):
      moves_found = {}
      for i in range(len(my_board)):
         for j in range(len(my_board[i])):
               flipped_stones = self.find_flipped(my_board, i, j, my_color)
               if len(flipped_stones) > 0:
                  moves_found.update({i*self.y_max+j: flipped_stones})
      return moves_found


   def inbounds(self, x, y):
      if 0 <= x <= self.x_max:
         if 0 <= y <= self.y_max:
            return True
      return False