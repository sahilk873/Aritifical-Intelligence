# Name:          Date:
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

def check_adj(words_set):
   # This check method is written for words_6_longer.txt
   adj = generate_adjacents('listen', words_set)
   target =  {'listee', 'listel', 'litten', 'lister', 'listed'}
   return (adj == target)

def bi_bfs(start, goal, words_set):
   '''The idea of bi-directional search is to run two simultaneous searches--
   one forward from the initial state and the other backward from the goal--
   hoping that the two searches meet in the middle. 
   '''
   explored = {start: "s"}
   exploredend = {goal: "s"}
   t = ""
   s  = ""
   Q = [start]
   Qend = [goal]
   while(len(Q)!=0 and len(Qend) != 0):
        if(len(Q) != 0):
            s = Q.pop(0)
            for a in generate_adjacents(s, words_set):
                if a not in explored:
                    Q.append(a)
                    explored[a] = s
            if s in exploredend:
                x = list(generate_path(s, exploredend)[0])
                y = list(generate_path(s, explored)[0])
                x = x[::-1]
                z = y[:-1]+x
                return z

        if(len(Qend) != 0):
            s = Qend.pop(0)
            for a in generate_adjacents(s, words_set):
                if a not in exploredend:
                    Qend.append(a)
                    exploredend[a] = s
            if s in explored:
                x = list(generate_path(s, exploredend)[0])
                y = list(generate_path(s, explored)[0])
                x = x[::-1]
                z = y[:-1] + x
                return z
      
   # goal test is passed? return explored, ""
   return (["No solution"], 0)

def generate_path(current, explored):
   list = [current]
   count = 0
   while explored[current] != "s":       #assume the parent of root is "s"
      list.append(explored[current])
      current = explored[current]
      count += 1
   return (list[::-1], count+1)

def main():
   filename = input("Type the word file: ")
   words_set = set()
   file = open(filename, "r")
   for word in file.readlines():
      words_set.add(word.rstrip('\n'))
   #print ("Check generate_adjacents():", check_adj(words_set))
   initial = input("Type the starting word: ")
   goal = input("Type the goal word: ")
   cur_time = time.time()
   path = (bi_bfs(initial, goal, words_set))
   if path != None:
      print (path)
      print ("The number of steps: ", len(path))
      print ("Duration: ", time.time() - cur_time)
   else:
      print ("There's no path")
 
#if __name__ == '__main__':
   #main()

'''
Sample output 1
Type the word file: words.txt
Type the starting word: listen
Type the goal word: beaker
['listen', 'listed', 'fisted', 'fitted', 'fitter', 'bitter', 'better', 'beater', 'beaker']
The number of steps:  9
Duration: 0.0

Sample output 2
Type the word file: words_6_longer.txt
Type the starting word: listen
Type the goal word: beaker
['listen', 'lister', 'bister', 'bitter', 'better', 'beater', 'beaker']
The number of steps:  7
Duration: 0.000997304916381836

Sample output 3
Type the word file: words_6_longer.txt
Type the starting word: vaguer
Type the goal word: drifts
['vaguer', 'vagues', 'values', 'valves', 'calves', 'cauves', 'cruves', 'cruses', 'crusts', 'crufts', 'crafts', 'drafts', 'drifts']
The number of steps:  13
Duration: 0.0408782958984375

Sample output 4
Type the word file: words_6_longer.txt
Type the starting word: klatch
Type the goal word: giggle
['klatch', 'clatch', 'clutch', 'clunch', 'glunch', 'gaunch', 'paunch', 'paunce', 'pawnce', 'pawnee', 'pawned', 'panned', 'panged', 'ranged', 'ragged', 'raggee', 'raggle', 'gaggle', 'giggle']
The number of steps:  19
Duration:  0.0867915153503418
'''
