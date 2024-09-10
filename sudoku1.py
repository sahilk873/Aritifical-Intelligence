import time
import sys; args = sys.argv[1:]
puzzles = open("puzzles.txt").read().splitlines()




neighbors = {0: {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 18, 19, 20, 27, 36, 45, 54, 63, 72}, 1: {0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 18, 19, 20, 28, 37, 46, 55, 64, 73}, 2: {0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 18, 19, 20, 29, 38, 47, 56, 65, 74}, 3: {0, 1, 2, 4, 5, 6, 7, 8, 12, 13, 14, 21, 22, 23, 30, 39, 48, 57, 66, 75}, 4: {0, 1, 2, 3, 5, 6, 7, 8, 12, 13, 14, 21, 22, 23, 31, 40, 49, 58, 67, 76}, 5: {0, 1, 2, 3, 4, 6, 7, 8, 12, 13, 14, 21, 22, 23, 32, 41, 50, 59, 68, 77}, 6: {0, 1, 2, 3, 4, 5, 7, 8, 15, 16, 17, 24, 25, 26, 33, 42, 51, 60, 69, 78}, 7: {0, 1, 2, 3, 4, 5, 6, 8, 15, 16, 17, 24, 25, 26, 34, 43, 52, 61, 70, 79}, 8: {0, 1, 2, 3, 4, 5, 6, 7, 15, 16, 17, 24, 25, 26, 35, 44, 53, 62, 71, 80}, 9: {0, 1, 2, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 27, 36, 45, 54, 63, 72}, 10: {0, 1, 2, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 28, 37, 46, 55, 64, 73}, 11: {0, 1, 2, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 29, 38, 47, 56, 65, 74}, 12: {3, 4, 5, 9, 10, 11, 13, 14, 15, 16, 17, 21, 22, 23, 30, 39, 48, 57, 66, 75}, 13: {3, 4, 5, 9, 10, 11, 12, 14, 15, 16, 17, 21, 22, 23, 31, 40, 49, 58, 67, 76}, 14: {3, 4, 5, 9, 10, 11, 12, 13, 15, 16, 17, 21, 22, 23, 32, 41, 50, 59, 68, 77}, 15: {6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 24, 25, 26, 33, 42, 51, 60, 69, 78}, 16: {6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 24, 25, 26, 34, 43, 52, 61, 70, 79}, 17: {6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 24, 25, 26, 35, 44, 53, 62, 71, 80}, 18: {0, 1, 2, 9, 10, 11, 19, 20, 21, 22, 23, 24, 25, 26, 27, 36, 45, 54, 63, 72}, 19: {0, 1, 2, 9, 10, 11, 18, 20, 21, 22, 23, 24, 25, 26, 28, 37, 46, 55, 64, 73}, 20: {0, 1, 2, 9, 10, 11, 18, 19, 21, 22, 23, 24, 25, 26, 29, 38, 47, 56, 65, 74}, 
   21: {3, 4, 5, 12, 13, 14, 18, 19, 20, 22, 23, 24, 25, 26, 30, 39, 48, 57, 66, 75}, 22: {3, 4, 5, 12, 13, 14, 18, 19, 20, 21, 23, 24, 25, 26, 31, 40, 49, 58, 67, 76}, 23: {3, 4, 5, 12, 13, 14, 18, 19, 20, 21, 22, 24, 25, 26, 32, 41, 50, 59, 68, 77}, 24: {6, 7, 8, 15, 16, 17, 18, 19, 20, 21, 22, 23, 25, 26, 33, 42, 51, 60, 69, 78}, 25: {6, 7, 8, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 26, 34, 43, 52, 61, 70, 79}, 26: {6, 7, 8, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 35, 44, 53, 62, 71, 80}, 27: {0, 9, 18, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 45, 46, 47, 54, 63, 72}, 28: {1, 10, 19, 27, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 45, 46, 47, 55, 64, 73}, 29: {2, 11, 20, 27, 28, 30, 31, 32, 33, 34, 35, 36, 37, 38, 45, 46, 47, 56, 65, 74}, 30: {3, 12, 21, 27, 28, 29, 31, 32, 33, 34, 35, 39, 40, 41, 48, 49, 50, 57, 66, 75}, 31: {4, 13, 22, 27, 28, 29, 30, 32, 33, 34, 35, 39, 40, 41, 48, 49, 50, 58, 67, 76}, 32: {5, 14, 23, 27, 28, 29, 30, 31, 33, 34, 35, 39, 40, 41, 48, 49, 50, 59, 68, 77}, 33: {6, 15, 24, 27, 28, 29, 30, 31, 32, 34, 35, 42, 43, 44, 51, 52, 53, 60, 69, 78}, 34: {7, 16, 25, 27, 28, 29, 30, 31, 32, 33, 35, 42, 43, 44, 51, 52, 53, 61, 70, 79}, 35: {8, 17, 26, 27, 28, 29, 30, 31, 32, 33, 34, 42, 43, 44, 51, 52, 53, 62, 71, 80}, 36: {0, 9, 18, 27, 28, 29, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 54, 63, 72}, 37: {1, 10, 19, 27, 28, 29, 36, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 55, 64, 73}, 38: {2, 11, 20, 27, 28, 29, 36, 37, 39, 40, 41, 42, 43, 44, 45, 46, 47, 56, 65, 74}, 39: {3, 12, 21, 30, 31, 32, 36, 37, 38, 40, 41, 42, 43, 44, 48, 49, 50, 57, 66, 75}, 40: {4, 13, 22, 30, 31, 32, 36, 37, 38, 39, 41, 42, 43, 44, 48, 49, 50, 58, 67, 76}, 
   41: {5, 14, 23, 30, 31, 32, 36, 37, 38, 39, 40, 42, 43, 44, 48, 49, 50, 59, 68, 77}, 42: {6, 15, 24, 33, 34, 35, 36, 37, 38, 39, 40, 41, 43, 44, 51, 52, 53, 60, 69, 78}, 43: {7, 16, 25, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 44, 51, 52, 53, 61, 70, 79}, 44: {8, 17, 26, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 51, 52, 53, 62, 71, 80}, 45: {0, 9, 18, 27, 28, 29, 36, 37, 38, 46, 47, 48, 49, 50, 51, 52, 53, 54, 63, 72}, 46: {1, 10, 19, 27, 28, 29, 36, 37, 38, 45, 47, 48, 49, 50, 51, 52, 53, 55, 64, 73}, 47: {2, 11, 20, 27, 28, 29, 36, 37, 38, 45, 46, 48, 49, 50, 51, 52, 53, 56, 65, 74}, 48: {3, 12, 21, 30, 31, 32, 39, 40, 41, 45, 46, 47, 49, 50, 51, 52, 53, 57, 66, 75}, 49: {4, 13, 22, 30, 31, 32, 39, 40, 41, 45, 46, 47, 48, 50, 51, 52, 53, 58, 67, 76}, 50: {5, 14, 23, 30, 31, 32, 39, 40, 41, 45, 46, 47, 48, 49, 51, 52, 53, 59, 68, 77}, 51: {6, 15, 24, 33, 34, 35, 42, 43, 44, 45, 46, 47, 48, 49, 50, 52, 53, 60, 69, 78}, 52: {7, 16, 25, 33, 34, 35, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 53, 61, 70, 79}, 53: {8, 17, 26, 33, 34, 35, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 62, 71, 80}, 54: {0, 9, 18, 27, 36, 45, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 72, 73, 74}, 55: {1, 10, 19, 28, 37, 46, 54, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 72, 73, 74}, 56: {2, 11, 20, 29, 38, 47, 54, 55, 57, 58, 59, 60, 61, 62, 63, 64, 65, 72, 73, 74}, 57: {3, 12, 21, 30, 39, 48, 54, 55, 56, 58, 59, 60, 61, 62, 66, 67, 68, 75, 76, 77}, 58: {4, 13, 22, 31, 40, 49, 54, 55, 56, 57, 59, 60, 61, 62, 66, 67, 68, 75, 76, 77}, 59: {5, 14, 23, 32, 41, 50, 54, 55, 56, 57, 58, 60, 61, 62, 66, 67, 68, 75, 76, 77}, 60: {6, 15, 24, 33, 42, 51, 54, 55, 56, 57, 58, 59, 61, 62, 69, 70, 71, 78, 79, 80}, 
   61: {7, 16, 25, 34, 43, 52, 54, 55, 56, 57, 58, 59, 60, 62, 69, 70, 71, 78, 79, 80}, 62: {8, 17, 26, 35, 44, 53, 54, 55, 56, 57, 58, 59, 60, 61, 69, 70, 71, 78, 79, 80}, 63: {0, 9, 18, 27, 36, 45, 54, 55, 56, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74}, 64: {1, 10, 19, 28, 37, 46, 54, 55, 56, 63, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74}, 65: {2, 11, 20, 29, 38, 47, 54, 55, 56, 63, 64, 66, 67, 68, 69, 70, 71, 72, 73, 74}, 66: {3, 12, 21, 30, 39, 48, 57, 58, 59, 63, 64, 65, 67, 68, 69, 70, 71, 75, 76, 77}, 67: {4, 13, 22, 31, 40, 49, 57, 58, 59, 63, 64, 65, 66, 68, 69, 70, 71, 75, 76, 77}, 68: {5, 14, 23, 32, 41, 50, 57, 58, 59, 63, 64, 65, 66, 67, 69, 70, 71, 75, 76, 77}, 69: {6, 15, 24, 33, 42, 51, 60, 61, 62, 63, 64, 65, 66, 67, 68, 70, 71, 78, 79, 80}, 70: {7, 16, 25, 34, 43, 52, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 71, 78, 79, 80}, 71: {8, 17, 26, 35, 44, 53, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 78, 79, 80}, 72: {0, 9, 18, 27, 36, 45, 54, 55, 56, 63, 64, 65, 73, 74, 75, 76, 77, 78, 79, 80}, 73: {1, 10, 19, 28, 37, 46, 54, 55, 56, 63, 64, 65, 72, 74, 75, 76, 77, 78, 79, 80}, 74: {2, 11, 20, 29, 38, 47, 54, 55, 56, 63, 64, 65, 72, 73, 75, 76, 77, 78, 79, 80}, 75: {3, 12, 21, 30, 39, 48, 57, 58, 59, 66, 67, 68, 72, 73, 74, 76, 77, 78, 79, 80}, 76: {4, 13, 22, 31, 40, 49, 57, 58, 59, 66, 67, 68, 72, 73, 74, 75, 77, 78, 79, 80}, 77: {5, 14, 23, 32, 41, 50, 57, 58, 59, 66, 67, 68, 72, 73, 74, 75, 76, 78, 79, 80}, 78: {6, 15, 24, 33, 42, 51, 60, 61, 62, 69, 70, 71, 72, 73, 74, 75, 76, 77, 79, 80}, 79: {7, 16, 25, 34, 43, 52, 60, 61, 62, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 80}, 80: {8, 17, 26, 35, 44, 53, 60, 61, 62, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79}}
   
csp_table = [{0, 1, 2, 9, 10, 11, 18, 19, 20}, {0, 9, 18, 27, 36, 45, 54, 63, 72}, {0, 1, 2, 3, 4, 5, 6, 7, 8}, {3, 4, 5, 12, 13, 14, 21, 22, 23}, {1, 10, 19, 28, 37, 46, 55, 64, 73}, {9, 10, 11, 12, 13, 14, 15, 16, 17}, {6, 7, 8, 15, 16, 17, 24, 25, 26}, {2, 11, 20, 29, 38, 47, 56, 65, 74}, {18, 19, 20, 21, 22, 23, 24, 25, 26}, {27, 28, 29, 36, 37, 38, 45, 46, 47}, {3, 12, 21, 30, 39, 48, 57, 66, 75}, {27, 28, 29, 30, 31, 32, 33, 34, 35}, {30, 31, 32, 39, 40, 41, 48, 49, 50}, {4, 13, 22, 31, 40, 49, 58, 67, 76}, {36, 37, 38, 39, 40, 41, 42, 43, 44}, {33, 34, 35, 42, 43, 44, 51, 52, 53}, {5, 14, 23, 32, 41, 50, 59, 68, 77}, {45, 46, 47, 48, 49, 50, 51, 52, 53}, {54, 55, 56, 63, 64, 65, 72, 73, 74}, {6, 15, 24, 33, 42, 51, 60, 69, 78}, {54, 55, 56, 57, 58, 59, 60, 61, 62}, {57, 58, 59, 66, 67, 68, 75, 76, 77}, {7, 16, 25, 34, 43, 52, 61, 70, 79}, {63, 64, 65, 66, 67, 68, 69, 70, 71}, {60, 61, 62, 69, 70, 71, 78, 79, 80}, {8, 17, 26, 35, 44, 53, 62, 71, 80}, {72, 73, 74, 75, 76, 77, 78, 79, 80}]

allvariables = {"1", "2", "3", "4", "5", "6", "7", "8", "9"} 




#eliminate values constrained in initial variables and if the length of the new variables is zero update original puzzle
#once i found new value to constrain, constraint the new variables, maybe only add final values to assignment after for loop is over

def run(assignment):
   freq_table, variables = helper(assignment, neighbors)
   return recursive_backtracking(assignment, variables, csp_table, neighbors, freq_table)


def helper(assignment, neighbors):
   initial = {}
   freq_table = {0:1, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
   for i in range(len(assignment)):
      if assignment[i] == ".":
         temp = set()
         for b in neighbors[i]:
            temp.add(assignment[b])
         initial[i] = allvariables - temp
         if(len(initial[i]) == 1):
            for item in initial[i]:
               update = list(assignment)
               update[i] = item
               assignment = "".join(update)
               freq_table[int(item)] += 1
      else:
         freq_table[int(assignment[i])] += 1
   return freq_table, initial

      


'''
def forward(assignment, freq_table):
   totalcounter = 0
   for constraint in csp_table:
      counter = 0
      values = set()
      noval = 0
      for term in constraint:
         if assignment[term] != '.':
            values.add(assignment[term])
            counter += 1
         else:
            noval = term
      if counter == 8:
         totalcounter += 1
         value = (allvariables - values).pop()
         l = list(assignment)
         l[noval] = value
         assignment = "".join(l)
         freq_table[int(value)] += 1
   
      return assignment
'''

def check_complete(assignment, csp_table):
   if assignment.find('.') != -1: return False
   return True
            
'''
def select_unassigned_var(assignment, variables, csp_table):
   min_val, index = 9999, -1
   for i in range(len(assignment)):
      if assignment[i] == '.' and len(variables[i]) < min_val:
            min_val = len(variables[i])
            index = i
   return index
'''

def select_unassigned_var(assignment, variables, csp_table):
   min_val, index = 9999, -1
   for i in range(len(assignment)):
      if assignment[i] == '.':
         if len(variables[i]) < min_val:
            min_val = len(variables[i])
            index = i
   return index

         


def isInvalid(value, var_index, puzzle, neighbors):
   for i in neighbors[var_index]:
      if puzzle[i] == str(value):
         return True
   return False

'''
def ordered_domain(var_index, assignment, variables, csp_table):
   freq = []
   for x in (range(1, 10)):
      freq.append(assignment.count(str(x)))
   x = zip(freq, list(range(1, 10)))
   sort = sorted(x, reverse=True)
   final = []
   for term in sort:
      final.append(term[1])
   return final
'''

def ordered_domain(freq_table):
   temp2 = sorted(([(c, value) for value, c in freq_table.items()]), reverse = True)
   return [val for c, val in temp2]


def update_variables(value, var_index, assignment, variables, neighbors):
   updated = {k: list(variables[k]) for k in variables}
   for i in neighbors[var_index]:
      if i in updated and value in updated[i]:
         updated[i].remove(value)
      
   return updated
      
def recursive_backtracking(assignment, variables, csp_table, neighbors, freq_table):
   if check_complete(assignment, csp_table):
      return assignment

   var = select_unassigned_var(assignment, variables, csp_table)

   for value in ordered_domain(freq_table):
      if str(value) in variables[var]:
         if not isInvalid(value, var, assignment, neighbors):
            val = str(value)
            freq_table[int(val)] += 1
            assignment =  assignment[:var] + val + assignment[var + 1:]
            version = update_variables(value, var, assignment, variables, neighbors)
            outcome = recursive_backtracking(assignment, version, csp_table, neighbors, freq_table)
            if outcome != None: return outcome
            assignment = assignment[:var] + '.' + assignment[var + 1:]
            freq_table[int(val)] -= 1

   return None

def display(solution, csp_table):
   outcome = ""
   nline = '\n'
   space = " "
   for r in range(9):
      for c in range(9):
         outcome += solution[(r*9)+c] + space
         if c == 2 or c == 5:
            outcome += space
      outcome += nline
      if r == 2 or r == 5:
         outcome += nline
   return outcome


'''
def initial_variables(puzzle, csp_table):
   v = {}
   for a in range(81):
      if puzzle[a] == ".":
         temp = set()
         for b in neighbors[a]:
            temp.add(puzzle[b])
         v[a] = {"1", "2", "3", "4", "5", "6", "7", "8", "9"} - temp
   return v
'''


def checksum(solution):
   return sum([ord(c) for c in solution]) - 48*81 # One easy way to check a valid solution

   
def main():
   start = time.time()
   for line, puzzle in enumerate(puzzles):
      line, puzzle = line+1, puzzle.rstrip()
      #if line == 51: 
         #break
      print ("{}: {}".format(line, puzzle))
      
      solution = run(puzzle)
      if solution == None:print ("No solution found."); break
      print ("{}{} {}".format(" "*(len(str(line))+2), solution, checksum(solution)))
      print(time.time() - start)



if __name__ == '__main__': main()
