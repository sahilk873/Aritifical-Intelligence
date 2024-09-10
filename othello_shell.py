# Name:
# Date:

import math
import random
import copy

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

   
   
class Best_AI_bot:

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
      searchdepth = 0
      piecesleft=self.placedstones(board, color)[0]
      searchdepth=4
      if piecesleft <30:
         searchdepth = 4
      if piecesleft<12:
         searchdepth=6
      if piecesleft < 6:
         v, move = self.minimax(board, color, 6)
         if move < 0 or move > 63 or board[move//8][move%8] != '.':
            d = self.find_moves(board, color)
            moves = list(d.keys())
            move = random.choice(moves)
         return (move//self.x_max, move % self.y_max), 0
      beta = 999999999999999
      v, move = self.alphabeta(board, color, searchdepth, -beta, beta)
      if move < 0 or move > 63 or board[move//8][move%8] != '.':
         d = self.find_moves(board, color)
         moves = list(d.keys())
         move = random.choice(moves)
      x, y = move//self.x_max, move%self.y_max
      return [x, y], v

   def alphabeta(self, board, color, depth, alpha, beta):
      if depth <= 0 or self.stones_left(board) == 0:
         return self.evaluate(board, color), 0
      if depth in (0, 2, 4, 6, 8, 10):         
         v, state=-9999999999, 15632241563224
         m=self.find_moves(board, color)
         for move in m:
            mv, ms= self.alphabeta(self.make_move(board, color, move, m[move]), self.opposite_color[color], depth - 1, alpha, beta)
            if v<mv:
               v, state=mv, move
            if v>beta:
               return v, state
            alpha=max(alpha, v)
         return v, state
      else:
         v, state= 9999999999, 15632241563224
         m=self.find_moves(board, color)
         for move in m:
            mv, ms=self.alphabeta(self.make_move(board, color, move, m[move]), self.opposite_color[color], depth-1, alpha, beta)
            if v>mv:
               v, state= mv, move
            if v<alpha:
               return v, state
            beta=min(beta, v)
         return v, state
   def minimax(self, board, color, search_depth):
      return self.max_value(board, color, search_depth)

   def max_value(self, board, color, search_depth):
      if search_depth <= 0 or self.stones_left(board) == 0:
         return self.evaluate(board, self.color), 0
      v = -1000000000000
      state = 0
      m = self.find_moves(board, color)
      for move in m:
         newboard = self.make_move(board, color, move, m[move])
         newdepth = search_depth - 1
         mv, ms = self.min_value(newboard, self.opposite_color[color], newdepth)
         if v < mv:
            v = mv
            state = move
      return v, state

   def min_value(self, board, color, search_depth):
      if search_depth <= 0 or self.stones_left(board) == 0:
         return self.evaluate(board, self.color), 0
      v = 1000000000000
      state = 0
      m = self.find_moves(board, color)
      for move in m:
         newboard = self.make_move(board, color, move, m[move])
         newdepth = search_depth - 1
         mv, ms = self.max_value(newboard, self.opposite_color[color], newdepth)
         if v > mv:
            v = mv
            state = move
      return v, state
         

   def make_move(self, board, color, move, flipped):
      newboard = [row[:] for row in board]
      x, y = move//8, move%8
      newboard[x][y]=color
      for flips in flipped:
         newboard[flips[0]][flips[1]]=color
      return newboard

   def placedstones(self, board, color):
      player=0
      opp=0
      for i in range(len(board)):
         for j in range(len(board[i])):
            if board[i][j] == color:
               player += 1
            if board[i][j] == self.opposite_color[color]:
               opp += 1
      return 64-(player + opp), player, opp

   def evaluate(self, board, color):   
      piecesleft, pmaterial, oppmaterial= self.placedstones(board, color)
      parity = pmaterial - oppmaterial
      if piecesleft==0:
         return 5000*(parity)
      opponent=self.opposite_color[color]
      mobility=len(self.find_moves(board, color)) - len(self.find_moves(board, opponent))
      corner=0
      for i in [0, len(board)-1]:
         for j in [0, len(board[i])-1]:
            if board[i][j]==color:
               corner+=1   
            if board[i][j]==opponent:
               corner-=1
      adjcount = self.adjcount1(board, color, opponent)
      adjcount1 = self.adjcount2(board, color, opponent)
      adjcount = adjcount - adjcount1
      stability_weights = [
    [20, -5, 10, 8, 8, 10, -5, 20],
    [-5, -7, -5, 2, 2, -5, -7, -5],
    [10, -5, 3, 3, 3, 3, -5, 10],
    [8, 2, 3, 0, 0, 3, 2, 8],
    [8, 2, 3, 0, 0, 3, 2, 8],
    [10, -5, 3, 3, 3, 3, -5, 10],
    [-5, -7, -5, 2, 2, -5, -7, -5],
    [20, -5, 10, 8, 8, 10, -5, 20]
]
      sweight = 1.5
      turn_count = 64-piecesleft
      stability = 0
      threat = self.threat_eval(board, color, opponent)
      for row in range(8):
         for col in range(8):
               if board[row][col] == color:
                  stability += stability_weights[row][col] * (1 - (turn_count / 100))
               elif board[row][col] == opponent:
                  stability -= stability_weights[row][col] * (1 - (turn_count / 100))
      if piecesleft<8:
         return (parity * 10) + (corner*100) + mobility + (adjcount * 10)
      if piecesleft > 56:
         return (corner * 100) + (mobility * 50) + (adjcount * 10)
      if piecesleft>30:
         return (mobility * 2) + (corner * 100) + (-1*parity) + (adjcount * 8) + stability*(sweight)
      
      return mobility*2+100*corner+10*adjcount

   def adjcount1(self, board, color, opponent):
      adjcount = 0
      for (i, j) in [(0, 1), (1, 1), (1, 0), (0, 6), (1, 6), (1, 7), (7, 6), (6, 7), (6, 6), (6, 1), (7, 1), (6, 0)]:
         if board[i][j] == color and (board[0][0] == opponent or board[0][0] == ".") or (board[0][7] == opponent or board[0][7] == ".") or (board[7][0] == opponent or board[7][0] == ".") or (board[7][7] == opponent or board[7][7] == "."):
            adjcount -= 1
      return adjcount
   
   def adjcount2(self, board, color, opponent):
      adjcount = 0
      for (i, j) in [(1, 7), (6, 1), (7, 1), (0, 1), (1, 1), (1, 0), (0, 6), (1, 6), (6, 0), (7, 6), (6, 7), (6, 6)]:
         if board[i][j] == color and (board[0][0] == color or board[0][7] == color or board[7][0] == color or board[7][7] == color) or (board[i][j] == opponent and (board[0][0] == "." or board[0][7] == "." or board[7][0] == "." or board[7][7] == ".")):
            adjcount += 1
      return adjcount
      
   def threat_eval(self, board, color, opponent):
    threat_score = 0
    for row in range(8):
        for col in range(8):
            if board[row][col] == color:
                if row > 0 and board[row-1][col] == opponent:
                    threat_score += 1
                if row < 7 and board[row+1][col] == opponent:
                    threat_score += 1
                if col > 0 and board[row][col-1] == opponent:
                    threat_score += 1
                if col < 7 and board[row][col+1] == opponent:
                    threat_score += 1
    return threat_score

   def stones_left(self, board):
         stonesleft = 0
         for i in range(len(board)):
            for j in range(len(board)):
               if board[i][j] == '.':
                  stonesleft += 1
         return stonesleft

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
