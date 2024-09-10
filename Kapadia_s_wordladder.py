
import math
import time

alpha = "abcdefghijklmnopqrstuvwxyz"


def generate_adjacents(current, words_set):
   ''' words_set is a set which has all words.
   By comparing current and words in the words_set,
   generate adjacents set of current and return it'''
   adj_set = set()
   for i in range(0, 6):
        for letter in alpha:
            newword = current[:i] + letter + current[i+1:]
            if newword != current:
                if newword in words_set:
                    adj_set.add(newword)
   return adj_set

def generate_path(current, explored):
   list = [current]
   count = 0
   while explored[current] != "s":       #assume the parent of root is "s"
      list.append(explored[current])
      current = explored[current]
      count += 1
   return (list[::-1], count+1)


def BFS(start, end, word_dict):
   explored = {start: "s"}
   Q = [start]
   while(len(Q)!=0):
      s = Q.pop(0)
      if(s == end):
         return generate_path(s, explored)
      for a in generate_adjacents(s, word_dict):
         if a not in explored:
            Q.append(a)
            explored[a] = s
   # goal test is passed? return explored, ""
   return (["No solution"], 0)


def recur(start, end, word_dict, explored, limit):
    if start == end:
        return generate_path(start, explored)
    elif limit == 0:
        return None
    else:
        for words in generate_adjacents(start, word_dict):
            new_explored = {key:explored[key] for key in explored}
            new_explored[words] = start
            result = recur(words, end, word_dict, new_explored, limit-1)
            if result != None:
                return result
    

 
def DLS(start, end, word_dict, limit):
   explored = {start:"s"}
   return recur(start, end, word_dict, explored, limit-1)

def main():
   filename = input("Type the word file: ")
   words_set = set()
   file = open(filename, "r")
   for word in file.readlines():
      words_set.add(word.rstrip('\n'))

   # Test BFS
   initial = input("Type the starting word: ")
   goal = input("Type the goal word: ")
   path_and_steps = (BFS(initial, goal, words_set))
   if path_and_steps != None:
      print ("Path:", path_and_steps[0])
      print ("The number steps: {}".format(path_and_steps[1]))
   else:
      print ("Solution not found in {} steps".format(limit))
 
   # Test DLS
   initial = input("Type the starting word: ")
   goal = input("Type the goal word: ")
   limit = int(input("Type the limit: "))
   path_and_steps = (DLS(initial, goal, words_set, limit))
   if path_and_steps != None:
      print ("Path:", path_and_steps[0])
      print ("steps within {} limit:".format(limit), path_and_steps[1])
   else:
      print ("Solution not found in {} steps".format(limit))
   
   # Now, start iterative deepening
   
   
   # Print out the shortest path and length of the path (number of steps)
   

if __name__ == '__main__':
   main()