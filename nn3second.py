#import sys; args = sys.argv[1:]
#infile = open(args[0])

import math, random


def transfer(t_funct, input):
   if t_funct == 'T3': 
       returnlist = []
       for x in input:
           try:
               returnlist.append(1 / (1 + math.e**-x))
           except OverflowError:
               if x > 0:
                     returnlist.append(1)
               else:
                     returnlist.append(0)
       return returnlist
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

def convergence_test(count, error, threshold):
    if count > 2500 and error > threshold:
        return True
    if error > 1000:
        return True
    return False

def gencase(n, radius, inequality):
    is_outside = random.choice([True, False])
    theta = random.random() * 2 * math.pi
    if is_outside:
        adjustment = random.uniform(radius, radius + 0.01)
    else:
        adjustment = random.uniform(0, radius - 0.01)
    x = adjustment * math.cos(theta)
    y = adjustment * math.sin(theta)
    if inequality == "less":
        if x*x + y*y <= radius*radius:
            target = 1
        else:
            target = 0
    else:
        if x*x + y*y >= radius*radius:
            target = 1
        else:
            target = 0
    return [x, y, target]

def correct(ts, xv, weights, t_funct):
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
    x, y, target = ts[0], ts[1], ts[2]
    if target == 1 and xv[-1][0] > 0.5:
        return True
    elif target == 0 and xv[-1][0] < 0.5:
        return True
    else:
        return False
    


def main():
   goof = 0
   t_funct = 'T3'  
   training_set = [[]]
   inequality = ""
   #eqn = args[0]
   eqn = "x*x+y*y<=1.21"
   #print(eqn)
   if eqn.find('<') != -1:
      inequality = 'less'
   else:
      inequality = 'great'
   if eqn.find('=') != -1:
      r = float(eqn[9:])
   else: 
      r = float(eqn[8:])
   r = math.sqrt(r)
   input, output = 2, 1
   for i in range(100000):
        training_set.append(gencase(i, r, inequality))
   training_set = training_set[1:]
   #layer_counts = [3, 4, 2, 1]
   layer_counts = [3, 10, 4, 1, 1]
   print ('layerCts:', layer_counts)
   
   weights = [[round(random.uniform(-2.0, 2.0), 2) for j in range(layer_counts[i]*layer_counts[i+1])]  for i in range(len(layer_counts)-2)]
   weights.append([round(random.uniform(-2.0, 2.0), 2) for i in range(layer_counts[-1])])
   best_weights = weights
   training_set = training_set[1:]
   x_vals = [[temp[0:len(temp)-output]] for temp in training_set] 
   for i in range(len(training_set)):
      for j in range(len(layer_counts)):
         if j == 0: x_vals[i][j].append(1.0)
         else: x_vals[i].append([0 for temp in range(layer_counts[j])])
   
   E_vals = [[[*i] for i in j] for j in x_vals] 
   negative_grad = [[*i] for i in weights]  
   errors = [10]*len(training_set) 
   count = 1 
   #print(layer_counts)
   for k in range(len(training_set)):
      x_vals[k], errors[k] = ff(training_set[k], x_vals[k], weights, t_funct)
   err = sum(errors)
   init_err = err
   trial = 1
   besterr = err
   hold_err = err
   alpha = 5
   minweights = weights
   minerror = 99999999999999999999999999999999999999
   errlist = []
   errlist.append(err)
   #print('initial error', err)
   while err > 0.01:
        #print(trial)
        trial += 1
        for k in range(len(training_set)):
            learning_rate = 0.5 * (1 + math.cos(k / 1000 * math.pi)) * alpha
            E_vals[k], negative_grad = bp(training_set[k], x_vals[k], weights, E_vals[k], negative_grad)
            weights = update_weights(weights, negative_grad, learning_rate)
            if k % 1000 == 0:
                alpha = alpha * .8
            if err < besterr:
                besterr = err
            if err < 0.01:
                break
            if err > init_err:
                weights = [[round(random.uniform(-2.0, 2.0), 2) for j in range(layer_counts[i]*layer_counts[i+1])]  for i in range(len(layer_counts)-2)]
                weights.append([round(random.uniform(-2.0, 2.0), 2) for i in range(layer_counts[-1])])
                for k in range(len(training_set)):
                    x_vals[k], errors[k] = ff(training_set[k], x_vals[k], weights, t_funct)
                    init_err = sum(errors)
                    err = init_err                
        for i in range(len(training_set)):
                x_vals[i], errors[i] = ff(training_set[i], x_vals[i], weights, t_funct)
        err = sum(errors)
        if err < minerror:
            minerror = err
            minweights = weights 

        print(err)
    
#python nn2sahil.py x_gate_3.txt

   # print final weights of the working NN
   print ('weights:')
   for w in weights: print (w)
   #return weights
   #print('final error', err)
if __name__ == '__main__': main()

#Sahil Kapadia 7 2024


