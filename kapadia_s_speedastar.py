# Name:          Date:
from multiprocessing.heap import Heap
from operator import truediv
import random, time, math

class HeapPriorityQueue():
   def __init__(self):
      self.queue = ["dummy"]  # we do not use index 0 for easy index calulation
      self.current = 1        # to make this object iterable

   def next(self):            # define what __next__ does
      if self.current >=len(self.queue):
         self.current = 1     # to restart iteration later
         raise StopIteration
    
      out = self.queue[self.current]
      self.current += 1
   
      return out

   def __iter__(self):
      return self

   __next__ = next

   def isEmpty(self):
      return len(self.queue) <= 1    # b/c index 0 is dummy

   def swap(self, a, b):
      self.queue[a], self.queue[b] = self.queue[b], self.queue[a]

   # Add a value to the heap_pq
   def push(self, value):
      self.queue.append(value)
      self.heapUp(len(self.queue)-1)

   # helper method for push      
   def heapUp(self, k):
      parent = k//2
      if(parent<1):
        return;
      else:
        if(self.queue[k][0] > self.queue[parent][0]):
            return;
        else:
            self.swap(k, parent)
            self.heapUp(parent)

               
   # helper method for reheap and pop
   def heapDown(self, k, size):
      left  = 2*k
      right = (2*k)+1
      size = len(self.queue)
      if(k>=size):
         if(left >= size and right >= size):
            return;
      else:
         if(right<size):
            max = [left, right][self.queue[left][0] > self.queue[right][0]]
            if(self.queue[k][0]>self.queue[max][0]):
               self.swap(k, max)
               self.heapDown(max, size)
      
   # make the queue as a min-heap            
   def reheap(self):
      for i in range((len(self.queue)-1)//2, 0, -1):
         self.heapUp(i)
   
   # remove the min value (root of the heap)
   # return the removed value            
   def pop(self):
      self.swap(1, len(self.queue)-1)
      store = self.queue.pop(len(self.queue)-1)
      self.heapDown(1, len(self.queue)-1) # change this
      return store
      
   # remove a value at the given index (assume index 0 is the root)
   # return the removed value   
   def remove(self, index):
      
      # Your code goes here
      self.swap(index+1, len(self.queue)-1)
      store = self.queue.pop(len(self.queue)-1)
      self.heapDown(index+1, len(self.queue)-1)
      return store 

def inversion_count(new_state, width = 4, N = 4):
   inv = 0
   l = len(new_state)
   for i in range(l):
      for j in range(i, l):
         if new_state[i] != '_' and (new_state[i] > new_state[j]):
            inv += 1
   m = inv % 2
   r = new_state.find('_') // N
   if N % 2 == 0:
      if (r) % 2 == 0:
         return m % 2 == 0
      elif (r) % 2 != 0:
         return m % 2 != 0
   if N % 2 != 0:
      return m == 0
        
def check_inversion():
   t1 = inversion_count("_42135678", 3, 3)  # N=3
   f1 = inversion_count("21345678_", 3, 3)
   t2 = inversion_count("4123C98BDA765_EF", 4) # N is default, N=4
   f2 = inversion_count("4123C98BDA765_FE", 4)
   return t1 and t2 and not (f1 or f2)


def getInitialState(sample, size):
   sample_list = list(sample)
   random.shuffle(sample_list)
   new_state = ''.join(sample_list)
   while not inversion_count(new_state, size, size): 
      random.shuffle(sample_list)
      new_state = ''.join(sample_list)
   return new_state
   
def swap(n, i, j):
   condition = list(n)
   condition[i], condition[j] = condition[j], condition[i]
   s = "".join(condition)
   return s
      
'''Generate a list which hold all children of the current state
   and return the list'''
def generate_children(state, size=4):
   children = []
   blank = state.find('_')
   left = blank-1
   right = blank + 1
   up = blank - size
   down = blank + size
   if up >= 0:
        s = swap(state, blank, up)
        children.append(s)
   if down < len(state):
        s = swap(state, blank, down)
        children.append(s)
   x = right % size
   if x != 0:
        s = swap(state, blank, right)
        children.append(s)
   y = left % size
   if y != size - 1:
        s = swap(state, blank, left)
        children.append(s)
   return children

def display_path(path_list, size):
   for n in range(size):
      for path in path_list:
         print (path[n*size:(n+1)*size], end = " "*size)
      print ()
   print ("\nThe shortest path length is :", len(path_list))
   return ""

''' You can make multiple heuristic functions '''
def dist_heuristic(state, goal = "_123456789ABCDEF", size=4):
   # Your code goes here
   mandist = 0
   for i in range(len(state)):
      if state[i] != '_':
        g = goal.find(state[i])
        xcomp = abs(i%size - g%size)
        ycomp = abs(i//size - g//size)
        mandist += xcomp + ycomp

   return mandist


def check_heuristic():
   a = dist_heuristic("152349678_ABCDEF", "_123456789ABCDEF", 4)
   b = dist_heuristic("8936C_24A71FDB5E", "_123456789ABCDEF", 4)
   return (a < b) 

def solve(start, goal="_123456789ABCDEF", heuristic=dist_heuristic, size = 4):

      frontiers, explored = [], []
      frontiers.append(HeapPriorityQueue())
      frontiers.append(HeapPriorityQueue())
      explored.append({start:[[], 0]})
      explored.append({goal:[[], 0]})
      frontiers[0].push((heuristic(start, goal), start, [start]))
      frontiers[1].push((heuristic(goal, start), goal, [goal]))
      count = 1
      check1 = frontiers[0].isEmpty()
      check2 = frontiers[1].isEmpty()
      while not check1 and not check2:
         count = 1 - count
         otherf = 1-count
         s = frontiers[count].pop()
         node = s[1]
         if node in explored[otherf]:
            return s[2] + explored[otherf][node][0][:-1]
         for child in generate_children(node):
            pcost = len(s[2]) + 1
            if child not in explored[count]:
               np = s[2] + [child]
               if child not in explored[count]:
                  explored[count][child] = [np, pcost]
               explored[count][child][1] = pcost
               if count == 0:
                  heuristicv = heuristic(child, goal, size)    
               else:
                   heuristicv = heuristic(child, start, size)
               tpush = (pcost + heuristicv, child, np)
               frontiers[count].push(tpush)
            if pcost < explored[count][child][1]:
               np = s[2] + [child]
               if child not in explored[count]:
                  explored[count][child] = [np, pcost]
               explored[count][child][1] = pcost
               if count == 0:
                  heuristicv = heuristic(child, goal, size)    
               else:
                   heuristicv = heuristic(child, start, size)
               tpush = (pcost + heuristicv, child, np)
               frontiers[count].push(tpush)
            
      return None

def main():
    # A star
   print ("Inversion works?:", check_inversion())
   print ("Heuristic works?:", check_heuristic())
   #initial_state = getInitialState("_123456789ABCDEF", 4)
   initial_state = input("Type initial state: ")
   if inversion_count(initial_state):
      cur_time = time.time()
      path = (solve(initial_state))
      if path != None: display_path(path, 4)
      else: print ("No Path Found.")
      print ("Duration: ", (time.time() - cur_time))
   else: print ("{} did not pass inversion test.".format(initial_state))
   
if __name__ == '__main__':
   main()


''' Sample output 1

Inversion works?: True
Heuristic works?: True
Type initial state: 152349678_ABCDEF
1523    1523    1_23    _123    
4967    4_67    4567    4567    
8_AB    89AB    89AB    89AB    
CDEF    CDEF    CDEF    CDEF    

The shortest path length is : 4
Duration:  0.0


Sample output 2

Inversion works?: True
Heuristic works?: True
Type initial state: 2_63514B897ACDEF
2_63    _263    5263    5263    5263    5263    5263    5263    5263    52_3    5_23    _523    1523    1523    1_23    _123    
514B    514B    _14B    1_4B    14_B    147B    147B    147_    14_7    1467    1467    1467    _467    4_67    4567    4567    
897A    897A    897A    897A    897A    89_A    89A_    89AB    89AB    89AB    89AB    89AB    89AB    89AB    89AB    89AB    
CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    

The shortest path length is : 16
Duration:  0.005014657974243164


Sample output 3

Inversion works?: True
Heuristic works?: True
Type initial state: 8936C_24A71FDB5E
8936    8936    8936    893_    89_3    8943    8943    8_43    84_3    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    _423    4_23    4123    4123    4123    4123    _123    
C_24    C2_4    C24_    C246    C246    C2_6    C_26    C926    C926    C9_6    C916    C916    C916    C916    C916    C916    C916    C916    C916    _916    9_16    91_6    916_    9167    9167    9167    9167    9167    9167    _167    8167    8167    8_67    8567    8567    _567    4567    
A71F    A71F    A71F    A71F    A71F    A71F    A71F    A71F    A71F    A71F    A7_F    A_7F    AB7F    AB7F    AB7F    AB7_    AB_7    A_B7    _AB7    CAB7    CAB7    CAB7    CAB7    CAB_    CA_B    C_AB    C5AB    C5AB    _5AB    95AB    95AB    95AB    95AB    9_AB    _9AB    89AB    89AB    
DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    D_5E    D5_E    D5E_    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D_EF    _DEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    

The shortest path length is : 37
Duration:  0.27825474739074707


Sample output 4

Inversion works?: True
Heuristic works?: True
Type initial state: 8293AC4671FEDB5_
8293    8293    8293    8293    8293    8293    8293    8293    82_3    8_23    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    _423    4_23    4123    4123    4123    4123    _123    
AC46    AC46    AC46    AC46    AC46    _C46    C_46    C4_6    C496    C496    C_96    C9_6    C916    C916    C916    C916    C916    C916    C916    C916    C916    _916    9_16    91_6    916_    9167    9167    9167    9167    9167    9167    _167    8167    8167    8_67    8567    8567    _567    4567    
71FE    71F_    71_F    7_1F    _71F    A71F    A71F    A71F    A71F    A71F    A71F    A71F    A7_F    A_7F    AB7F    AB7F    AB7F    AB7_    AB_7    A_B7    _AB7    CAB7    CAB7    CAB7    CAB7    CAB_    CA_B    C_AB    C5AB    C5AB    _5AB    95AB    95AB    95AB    95AB    9_AB    _9AB    89AB    89AB    
DB5_    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    D_5E    D5_E    D5E_    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D_EF    _DEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    

The shortest path length is : 39
Duration:  0.7709157466888428

'''