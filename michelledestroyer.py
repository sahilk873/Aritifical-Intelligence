# Name:
# Date:

import math
import random

blank = '.'

class RandomBot:
   def __init__(self):
      self.white = "O"
      self.black = "@"
      self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
      self.opposite_color = {self.black: self.white, self.white: self.black}
      self.x_max = None
      self.y_max = None

   def best_strategy(self, board, color):
      # returns best move
      self.x_max = len(board)
      self.y_max = len(board[0])
      if color == "#000000":
         color = "@"
      else:
         color = "O"
      d = self.find_moves(board, color)
      moves = list(d.keys())
      r = random.choice(moves)
      x, y = r//8, r % 8

      ''' Your code goes here ''' 
      best_move = [x, y] # change this
      return best_move, 0

   def stones_left(self, board):
        remaining = 0
        for i in range(len(board)):
            for j in range(len(board)):
               if board[i][j] == '.':
                  remaining += 1
        return remaining

   def find_flipped(self, my_board, x, y, my_color):
    if my_board[x][y] != ".":
        return []
    if my_color == self.black:
        my_color = "@"
    else:
        my_color = "O"
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

   
   #count weight -1
class Best_AI_bot:

   def __init__(self):
      self.white = "O"
      self.black = "@"
      self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
      self.opposite_color = {self.black: self.white, self.white: self.black}
      self.x_max = None
      self.y_max = None

   def best_strategy(self, board, color):
    # returns best move
      self.x_max = len(board)
      self.y_max = len(board)
      if color == "#000000":
         color = "@"
      else:
         color = "O"
      searchdepth = 0
      if self.stones_left(board) > 30:
         searchdepth = 6
      if self.stones_left(board) > 15:
         searchdepth = 6
      else:
         searchdepth = 8
      move = -1
      alpha = -9999999999999999999999999999999
      beta = 999999999999999999999999999999
      possiblemoves = self.find_moves(board, color)
      v, move = self.alphabeta(board, color, searchdepth, alpha, beta, move)
      temp = [move//self.x_max,move%self.x_max]
      return temp, v

   def minimax(self, board, color, search_depth):
    # returns best "value"
      return 1
      
   def alphabeta(self, board, color, search_depth, alpha, beta, move):
      if search_depth <= 0 or self.stones_left(board) == 0:
         if self.stones_left(board) == 0:
            return self.evaluate(board, color, move), move
         return self.evaluate(board, color, move), 0
      if search_depth % 2 == 0:
         v = -999999999999999
         result = 1563224
         for move, stonesflipped in self.find_moves(board, color).items():
            mv, ms = self.alphabeta(self.make_move(board, color, move, stonesflipped), self.opposite_color[color], search_depth-1, alpha, beta, move)
            if v < mv or result == 1563224:
               v = mv
               result = move
            if v > beta:
               return v, result
            alpha = max(alpha, v)
         return v, result
      else:
         v = 999999999999999
         result = 1563224
         for move, stonesflipped in self.find_moves(board, color).items():
            mv, ms = self.alphabeta(self.make_move(board, color, move, stonesflipped), self.opposite_color[color], search_depth-1, alpha, beta, move)
            if v > mv or result == 1563224:
               v = mv
               result = move
            if v < alpha:
               return v, result
            beta = min(beta, v)
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

   def evaluate(self, board, color, last_move):
      score = self.score(board, color)
      return score
   
   
   def score(self, board, player):
      score = 0
      material, oppmaterial, left = self.placedstones(board, player)
      parity = material - oppmaterial
      if left == 0:
         return parity * 999999999
      opponent = self.opposite_color[player]
      mymoves = self.find_moves(board, player)
      oppmoves = self.find_moves(board, opponent)
      #determining mobility
      mobility = len(mymoves) - len(oppmoves)
      cornercount = 0
      #determining corner evaluation; maximize this
      for corner in (0, 7, 56, 63):
         x, y = corner//8, corner%8
         if board[x][y] == player:
            cornercount += 1
         if board[x][y] == opponent:
            cornercount -= 1
      #determining adjacent-corner evaluation: max this
      adjcount = 0
      corneradjlist =((0, 1, 8, 9), (7, 6, 14, 15), (56, 48, 49, 57), (63, 62, 54, 55))
      for term in corneradjlist:
         corner, adj1, adj2, adj3 = term
         iterate = (adj1, adj2, adj3)
         for adj1 in iterate:
            x, y = adj1//8, adj1%8
            cx, cy = corner//8, corner%8
            if (board[cx][cy] == opponent or board[cx][cy] == '.') and board[x][y] == player:
               adjcount -= 1
            if board[cx][cy] == player and board[x][y] == player or board[cx][cy] == opponent and board[x][y] == '.':
               adjcount += 1
      #middle16 positioning
      middlecount = 0
      middle = (24, 25, 26, 27, 32, 33, 34, 35, 40, 41, 42, 43, 48, 49, 50, 51, 17, 25, 33, 41, 22, 30, 38, 46)
      for i in range(8):
         for j in range(8):
            if board[i][j] == player and i*8+j in middle:
               middlecount +=1
            if board[i][j] == player and i*8+j not in middle:
               middlecount -= 1
               

      
      parity_weighting = 1
      mobility_weighting = 1
      cornercount_weighting = 100
      adjcount_weighting = 1
      middlecount_weighting = 1
      
      if left > 45:
         middlecount_weighting = 25
         mobility_weighting = 8
         parity_weighting = -20
         adjcount_weighting = 17
      if left > 20:
         middlecount_weighting = 0
         adjcount_weighting = 17
         parity_weighting = 2
         mobility_weighting = 45
      if left > 15:
         cornercount_weighting = 50
         mobility_weighting = 10
         middlecount_weighting = 0
         parity_weighting = 10
      if left > 6:
         middlecount_weighting = 0
         parity_weighting = 15
         

      score = (parity * parity_weighting) + (mobility_weighting * mobility) + (cornercount_weighting * cornercount) + (adjcount_weighting * adjcount) + (middlecount_weighting * middlecount)
      return score

      
   

   def placedstones(self, board, color):
      if color == self.black:
         symbol = 'x'
      else:
         symbol = 'o'
      counter = 0
      oppcounter = 0
      for i in range(len(board)):
         for j in range(len(board)):
            if board[i][j] == symbol:
               counter += 1
            if board[i][j] != '.':
               oppcounter +=1
      return counter, oppcounter, 64-(counter+oppcounter)

   def find_flipped(self, my_board, x, y, my_color):
    if my_board[x][y] != ".":
        return []
    if my_color == self.black:
        my_color = "@"
    else:
        my_color = "O"
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


class Alpha:

   def __init__(self):
      self.white = "O"
      self.black = "@"
      self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
      self.opposite_color = {self.black: self.white, self.white: self.black}
      self.x_max = None
      self.y_max = None
   
   def best_strategy(self, board, color):
      self.x_max = len(board)
      self.y_max = len(board[0])
      if color == "#000000":
         color = "@"
      else:
         color = "O"
      self.color = color
      num=self.count_each(board, color)[0]
      depth=6
      if num<15:
         depth=8
      v, state = self.alphabeta(board, color, depth, -9999999, 9999999)
      return (state//self.x_max, state%self.y_max), v

   '''def alphabeta(self, board, color, search_depth, alpha, beta):
      return self.max_value(board, 0, color, search_depth, alpha, beta)

   def max_value(self, board, move, color, deep, alpha, beta):
      opp=self.opposite_color[color]
      if deep<=0 or self.terminal_test(board, color):
         return self.evaluate(board, color), move
      v, state=-99999, move
      results=[]
      moves=self.find_moves(board, color)
      for move in moves:
         same= [row[:] for row in board]
         same=self.make_move(same, color, move, moves[move])
         val=self.min_value(same, move, opp, deep-1, alpha, beta)[0]
         alpha=max(alpha, val)
         results.append(val)
         if beta<=alpha:
            return max(results)
      return results

   def min_value(self, board, move, color, deep, alpha, beta):
      opp=self.opposite_color[color]
      if deep<=0 or self.terminal_test(board, color):
            return self.evaluate(board, color), move
      v, state=99999, move
      moves=self.find_moves(board, color)
      for move in moves:
         same= [row[:] for row in board]
         same=self.make_move(same, color, move, moves[move])
         val=self.max_value(same, move, opp, deep-1, alpha, beta)[0]
         if v>val:
            v, state=val, move
         if v<alpha:
            return v, state
         beta=min(beta, val)
      return v, state'''

   def alphabeta(self, board, color, deep, alpha, beta):
      work=self.terminal_test(board)
      if deep<=0 or work:
         return self.evaluate(board, color), 0
      if deep%2==1:         
         v, state= 9999999999, 0
         moves=self.find_moves(board, color)
         for move in moves:
            min_val=self.alphabeta(self.make_move(board, color, move, moves[move]), self.opposite_color[color], deep-1, alpha, beta)[0]
            if v>min_val:
               v, state= min_val, move
            if v<alpha:
               return v, state
            beta=min(beta, v)
         return v, state
      else:
         v, state=-9999999999, 0
         moves=self.find_moves(board, color)
         for move in moves:
            max_val= self.alphabeta(self.make_move(board, color, move, moves[move]), self.opposite_color[color], deep - 1, alpha, beta)[0]
            if v<max_val:
               v, state=max_val, move
            if v>beta:
               return v, state
            alpha=max(alpha, v)
         return v, state

   def make_move(self, board, color, move, flipped):
      copied = [row[:] for row in board]
      for flips in flipped:
         copied[flips[0]][flips[1]]=color
      copied[move//8][move%8]=color
      return copied

   def count_each(self, board, color):
      none=0
      player=0
      opp=0
      for i in range(len(board)):
         for j in range(len(board[i])):
            col=board[i][j]
            if col=='.':
               none+=1
            elif col==color:
               player+=1
            else:
               opp+=1
      return none, player, opp

   def evaluate(self, board, color):   
      open, player, opp= self.count_each(board, color)
      if open==0:
         return 5000*(player-opp)
      opp_col=self.opposite_color[color]
      moves=len(self.find_moves(board, color)) - len(self.find_moves(board, opp_col))
      corner=0
      for i in [0, len(board)-1]:
         for j in [0, len(board[i])-1]:
            if board[i][j]==color:
               corner+=1   
            if board[i][j]==opp_col:
               corner-=1
      near=0
      for (i, j) in [(0, 1), (1, 1), (1, 0)]:
         if board[i][j]==color and (board[0][0]==opp_col or board[0][0]=="."):
            near-=1
         if board[i][j]==color and board[0][0]==color or board[i][j]==opp_col and board[0][0]==".":
            near+=1
      for (i, j) in [(0, 6), (1, 6), (1, 7)]:
         if board[i][j]==color and (board[0][7]==opp_col or board[0][7]=="."):
            near-=1
         if board[i][j]==color and board[0][7]==color or board[i][j]==opp_col and board[0][7]==".":
            near+=1
      for (i, j) in [(6, 1), (7, 1), (6, 0)]:
         if board[i][j]==color and (board[7][0]==opp_col or board[7][0]=="."):
            near-=1
         if board[i][j]==color and board[7][0]==color or board[i][j]==opp_col and board[7][0]==".":
            near+=1
      for (i, j) in [(7, 6), (6, 7), (6, 6)]:
         if board[i][j]==color and (board[7][7]==opp_col or board[7][7]=="."):
            near-=1
         if board[i][j]==color and board[7][7]==color or board[i][j]==opp_col and board[7][7]==".":
            near+=1
      if open<10:
         return player-opp+corner*100+moves+8*near   
      if open>30:
         return moves*2+100*corner-(player-opp)+8*near
      return moves*2+100*corner+8*near

   def terminal_test(self, board):
      for i in range(len(board)):
         for j in range(len(board[i])):
            if board[i][j] == '.': return False
      return True

   def find_moves(self, my_board, my_color):
      moves_found = {}
      for i in range(len(my_board)):
         for j in range(len(my_board[i])):
            flipped_stones = self.find_flipped(my_board, i, j, my_color)
            if len(flipped_stones) > 0:
               moves_found.update({i*self.y_max+j: flipped_stones})
      return moves_found         

   def find_flipped(self, board, x, y, color):
      if board[x][y] != ".":
        return []
      if color == self.black:
        my_color = "@"
      else:
        my_color = "O"
      flipped_stones = []
      for incr in self.directions:
        temp_flip = []
        x_pos = x + incr[0]
        y_pos = y + incr[1]
        while 0 <= x_pos < self.x_max and 0 <= y_pos < self.y_max:
            if board[x_pos][y_pos] == ".":
                break
            if board[x_pos][y_pos] == my_color:
                flipped_stones += temp_flip
                break
            temp_flip.append([x_pos, y_pos])
            x_pos += incr[0]
            y_pos += incr[1]
      return flipped_stones
