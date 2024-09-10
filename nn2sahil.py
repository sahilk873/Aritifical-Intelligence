import sys; args = sys.argv[1:]
#infile = open(args[0])

import math, random


def transfer(t_funct, input):
   if t_funct == 'T3': return [1 / (1 + math.e**-x) for x in input]
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


def main():
   t_funct = 'T3'  
   training_set1 = [[]]
   input = 0
   output = 0
   f = open("x_gate_3.txt", "r")
   for line in f.readlines():
       temp = line.strip().split("=>")
       input, output = len(temp[0].split()), len(temp[1].split())
       training_set1.append(temp[0].split() + temp[1].split())
   for i in range(len(training_set1)):
       for j in range(len(training_set1[i])):
              training_set1[i][j] = float(training_set1[i][j])
   training_set1 = training_set1[1:]
   training_set = training_set1
   layer_counts = [input+1, output+1, output, output] 
   print ('layer counts', layer_counts)

   ''' build NN: x nodes and weights '''
   x_vals = [[temp[0:len(temp)-output]] for temp in training_set] 
   for i in range(len(training_set)):
      for j in range(len(layer_counts)):
         if j == 0: x_vals[i][j].append(1.0)
         else: x_vals[i].append([0 for temp in range(layer_counts[j])])
   
   weights = [[round(random.uniform(-2.0, 2.0), 2) for j in range(layer_counts[i]*layer_counts[i+1])]  for i in range(len(layer_counts)-2)]
   weights.append([round(random.uniform(-2.0, 2.0), 2) for i in range(layer_counts[-1])])



   E_vals = [[[*i] for i in j] for j in x_vals] 
   negative_grad = [[*i] for i in weights]  
   errors = [10]*len(training_set) 
   count = 1  
   alpha = 0.3
   
   print(layer_counts)

   for k in range(len(training_set)):
      x_vals[k], errors[k] = ff(training_set[k], x_vals[k], weights, t_funct)
   err = sum(errors)
   init_err = err
   print('initial error', err)
   errorthreshold = 0.01

   while err >= errorthreshold:
        for k in range(len(training_set)):
            E_vals[k], negative_grad = bp(training_set[k], x_vals[k], weights, E_vals[k], negative_grad)
            weights = update_weights(weights, negative_grad, max(0.5, 2/(count*.01 + 1)))

        for k in range(len(training_set)):
            x_vals[k], errors[k] = ff(training_set[k], x_vals[k], weights, t_funct)

        err = sum(errors)
        count += 1
        print(count, err)
        if convergence_test(count, err, 0.05) or count > 20000:  # Reset if not converging
            weights = [[round(random.uniform(-2.0, 2.0), 2) for j in range(layer_counts[i] * layer_counts[i+1])] for i in range(len(layer_counts) - 2)]
            weights.append([round(random.uniform(-2.0, 2.0), 2) for i in range(layer_counts[-1])])
            for k in range(len(training_set)):
                x_vals[k], errors[k] = ff(training_set[k], x_vals[k], weights, t_funct)
                init_err = sum(errors)
                err = init_err
                count = 1


   # print final weights of the working NN
   print ('final weights:')
   for w in weights: print (w)
   print('final error',err)
if __name__ == '__main__': main()


