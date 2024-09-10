#import sys; args = sys.argv[1].strip()

import math, random
  

def transfer(t_funct, input):
   if t_funct == 'T3': 
       answer = []
       for x in input:
           try:
                answer.append(1 / (1 + math.e**-x))
           except OverflowError:
                answer.append(0.000000000000000001)
       return answer
   elif t_funct == 'T4': return [-1+2/(1+math.e**-x) for x in input]
   elif t_funct == 'T2': return [x if x > 0 else 0 for x in input]
   else: return [x for x in input]

def dot_product(input, weights, stage):
   return [sum([input[x]*weights[x+s*len(input)] for x in range(len(input))]) for s in range(stage)]


def ff(ts, xv, weights, t_funct):
    for i in range(len(weights) - 1):
        nextneuron = xv[i+1]
        for j in range(len(nextneuron)):
            nextneuron[j] = 0
        for j in range(len(weights[i])):
            input_index = j % len(xv[i])  # Index of the input neuron within the previous layer
            output_index = j // len(xv[i])  # Index of the output neuron within the current layer
            nextneuron[output_index] += xv[i][input_index] * weights[i][j]
        xv[i + 1] = transfer(t_funct, nextneuron)
    for i in range(len(weights[-1])):
        xv[-1][i] = xv[-2][i] * weights[-1][i]
    err = sum([(ts[i-len(xv[-1])] - xv[-1][i])**2 for i in range(len(xv[-1]))]) / 2
    return xv, err

def bp(ts, xv, weights, ev, negative_grad):
    num_layers = len(weights)
    output = len(xv[num_layers])
    targets = [ts[-output:]]
    for x in range(len(targets[0])):
        ev[num_layers][x] = targets[0][x] - xv[num_layers][x]
        negative_grad[num_layers - 1][x] = xv[num_layers - 1][x] * ev[num_layers][x]
        ev[num_layers - 1][x] = negative_grad[num_layers - 1][x] * weights[num_layers - 1][x] * (1 - xv[num_layers - 1][x])
    for i in range(num_layers - 2, 0, -1):
        count = 0
        for x in range(len(xv[i]) * len(xv[i + 1])):
            negative_grad[i][x] = ev[i + 1][x // len(xv[i])] * xv[i][count]
            count = (count + 1) % len(xv[i])
        if len(xv[i + 1]) > 1:
            for x in range(len(xv[i])):
                tot = sum(negative_grad[i][x + count] * weights[i][x + count] * (1 - xv[i][x]) for count in range(0, len(xv[i]) * len(xv[i + 1]), len(xv[i])))
                ev[i][x] = tot
        else:
            for x in range(len(xv[i])):
                ev[i][x] = negative_grad[i][x] * weights[i][x] * (1 - xv[i][x])
    count = 0
    for x in range(len(xv[0]) * len(xv[1])):
        negative_grad[0][x] = ev[1][x // len(xv[0])] * xv[0][count]
        count = (count + 1) % len(xv[0])

    return ev, negative_grad


def update_weights(weights, negative_grad, alpha):

   ''' update weights (modify NN) code goes here '''
   for x in range(len(weights)):
      for y in range(len(weights[x])):
         weights[x][y] = (negative_grad[x][y]*alpha) + weights[x][y]
   return weights


def generateRandCase(n, radius, sign): # return [x, y] and whether or not
    # x, y always between -1.5, 1.5
    theta = random.random()*2*math.pi
    if n % 2: # return a pair within the circle
        randr = radius * random.uniform(0, 1)
        x = randr*math.cos(theta)
        y = randr*math.sin(theta)
    else: # return pair outside circle
        randr = radius * random.uniform(1, 1 + 1.5/radius)
        x = randr * math.cos(theta)
        y = randr * math.sin(theta)
    if sign == 'less':
        target = n % 2
    else:
        target = reverse(n % 2)
    return [x, y], target

def reverse(n):
    if n == 1: return 0
    else: return 1
    

weightStruct = [[1 for k in range(12)],
                [1 for k in range(8)],
                [1, 1],
                [1]]

nodeStruct = [[1, 1, 1], # inputs
              [0, 0, 0, 0], # layer 1 cells
              [0, 0],
              [0]] # layer 2

numCases = 1000

errList = [5 for k in range(numCases)]

def randomGenerateWeights(weights):
    for layer in weights:
        for weight in range(len(layer)):
            layer[weight] = random.randint(-2, 2)
    return weights

def calcError(target, result):
    return .5*(target - result)**2

def calcErrorList(errList):
    return sum(errList)/numCases



def main():
   t_funct = 'T3'  
   alpha = .1
   training_set1 = [[]]
   reset = 0
   resetErr = 0
   minError = 1
   minWeights = []
   minTestNum = 0
   minFF = []
   minErrList = []
   weights = randomGenerateWeights(weightStruct)
   inequality = ""
   #eqn = args
   eqn = "x*x+y*y>=1.21"
   print(eqn)
   if eqn.find('<') != -1:
      inequality = 'less'
   else:
      inequality = 'great'
   if eqn.find('=') != -1:
      r = float(eqn[9:])
   else: 
      r = float(eqn[8:])
   inputs, outputs = 2, 1
   for k in range(300000):
       inputs, target = generateRandCase(k, r, inequality)
       if not k % 1000: alpha = alpha * .975
       inputs.append(1)
       initial_nodes, result = ff(inputs, nodeStruct, weights, t_funct)
       result = result[0]
       err = calcError(target, result)
       print(err)
       tempErrList = [err for err in errList]
       tempErrList[k % numCases] = err
       newwErr = calcErrorList(tempErrList)
       newWeights = bp(inputs, initial_nodes, weights, err, t_funct)
       weights = newWeights
       tempNodes, checkResult = ff(target, [inputs], newWeights, t_funct)
       checkResult = checkResult[0]
       err = calcError(target, checkResult)
       print(err)
       tempErrList = [err for err in errList]
       tempErrList[k % numCases] = err
       newErr = calcErrorList(tempErrList)
       if k - reset > 20000 and newwErr - resetErr < .0001:
           reset = k
           resetErr = newwErr
           weights = randomGenerateWeights(weightStruct)
       if newwErr < minError:
           minError = newwErr
           minWeights = newWeights
           minTestNum = k
           minErrlist = errList
           minFF = initial_nodes
           if newErr < .001:
               print('layer cts: [{}, {}, {}, 1, 1]'
                  .format(len(nodeStruct[0]), len(nodeStruct[1]), len(nodeStruct[2])))
               for layer in newWeights:
                    print(layer)
               quit()

   '''# print final weights of the working NN
   print ('final weights:')
   for w in weights: print (w)
   print('final error',err)'''
if __name__ == '__main__': main()

#Sahil Kapadia 7 2024


