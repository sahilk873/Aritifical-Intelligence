import sys; args = sys.argv[1:]
infile = open(args[0])
import math, random, time

# t_funct is symbol of transfer functions: 'T1', 'T2', 'T3', or 'T4'
# input is a list of input (summation) values of the current layer
# returns a list of output values of the current layer
def transfer(t_funct, x):
   # if t_funct == 'T3': return [1 / (1 + math.e**-x) for x in input]
   # elif t_funct == 'T4': return [-1+2/(1+math.e**-x) for x in input]
   # elif t_funct == 'T2': return [x if x > 0 else 0 for x in input]
   # else: return [x for x in input]
   if t_funct == 'T3': return 1 / (1 + math.e**-x) 
   elif t_funct == 'T4': return -1+2/(1+math.e**-x) 
   elif t_funct == 'T2': return x if x > 0 else 0 
   else: return x

# returns a list of dot_product result. the len of the list == stage
# dot_product([x1, x2, x3], [w11, w21, w31, w12, w22, w32], 2) => [x1*w11 + x2*w21 + x3*w31, x1*w12, x2*w22, x3*w32] 
# def dot_product(input, weights, stage):
#    return [sum([input[x]*weights[x+s*len(input)] for x in range(len(input))]) for s in range(stage)]

def dot_product(input, weights):
   return sum(input[i] * weights[i] for i in range(len(weights)))

# Complete the whole forward feeding for one input(training) set
# return updated x_vals and error of the one forward feeding
def ff(ts, xv, weights, t_funct):

   ''' ff coding goes here '''

   for i in range(1, len(xv) - 1):
      for j in range(len(xv[i])):
         xv[i][j] = transfer(t_funct, dot_product(xv[i - 1], weights[i - 1][j * len(xv[i - 1]): (j + 1) * len(xv[i - 1])]))
   
   for j in range(len(xv[-1])):
      xv[-1][j] = xv[-2][j] * weights[-1][j]
   err = sum([(ts[i] - xv[-1][i])**2 for i in range(len(xv[-1]))]) / 2
   #err = sum([(ts[i-len(xv[-1])] - xv[-1][i])**2 for i in range(len(xv[-1]))]) / 2
   return xv, err

# Complete the back propagation with one training set and corresponding x_vals and weights
# update E_vals (ev) and negative_grad, and then return those two lists
def bp(ts, xv, weights, ev, negative_grad):   
   for i in range(len(ev[-1])):
      ev[-1][i] = ts[i] - xv[-1][i]
   
   for j in range(len(ev[-2])):
      ev[-2][j] = xv[-2][j] * (1 - xv[-2][j]) * ev[-1][j] * weights[-1][j]

   for i in range(len(xv) - 3, 0, -1):
      for j in range(len(ev[i])):
         #print(i, j, len(ev), len(ev[i]), len(ev[i + 1]), len(weights), len(weights[i]))
         ev[i][j] = xv[i][j] * (1 - xv[i][j]) * sum([ev[i + 1][k] * weights[i][k*len(ev[i]) + j] for k in range(len(ev[i + 1]))])
   
   #print(len(negative_grad), len(negative_grad[0]), len(xv), len(ev))
   for i in range(len(negative_grad)):
      for j in range(len(negative_grad[i])):
         #print(i, j, len(xv[i]), len(ev[i]))
         negative_grad[i][j] = xv[i][j % len(xv[i])] * ev[i + 1][j // len(ev[i])]
   ''' bp coding goes here '''
   return ev, negative_grad

# update all weights and return the new weights
# Challenge: one line solution is possible
def update_weights(weights, negative_grad, alpha):

   ''' update weights (modify NN) code goes here '''
   for i in range(len(weights)):
      for j in range(len(weights[i])):
         weights[i][j] += alpha * negative_grad[i][j]
   return weights

def main():
   t_funct = 'T3' # we default the transfer(activation) function as 1 / (1 + math.e**(-x))
   ''' work on training_set and layer_count '''
   training_set = []  # list of lists

   start = time.time()

   input = []
   output = []
   for l in infile.readlines():
      data = l.split(" ")
      print(data)
      i = data.index("=>")
      input.append([int(data[n]) for n in range(0, i)])
      output.append([int(data[n]) for n in range(i + 1, len(data))])

   print('input', input)
   print('output', output)

   #for i in range(len(input)): training_set.append(input[i] + output[i])

   #print (training_set) #[[1.0, -1.0, 1.0], [-1.0, 1.0, 1.0], [1.0, 1.0, 1.0], [-1.0, -1.0, 1.0], [0.0, 0.0, 0.0]]
   layer_counts = [len(input[0]) + 1, len(output[0]) + 1, len(output[0]), len(output[0])] # set the number of layers: (# of input + 1), (# of output + 1), # of output, # of output
   print ('layer counts', layer_counts) # This is the first output. [3, 2, 1, 1] with teh given x_gate.txt

   x_vals = []
   for i in range(len(output)):
      x_vals.append(list())
      for j in range(len(layer_counts)):
         if j == 0: x_vals[i].append([n for n in input[i]] + [1.0])
         else: x_vals[i].append([0 for _ in range(layer_counts[j])])

   # weights = []
   # for i in range(len(layer_counts) - 1):
   #    weights.append(list())
   #    for j in range(layer_counts[i] * layer_counts[i + 1]):
   #       weights[i].append(random.uniform(-1, 1))

   # print('weights', weights)

   ''' build NN: x nodes and weights '''
   # x_vals = [[temp[0:len(temp)-1]] for temp in training_set] # x_vals starts with first input values
   #print (x_vals) # [[[1.0, -1.0]], [[-1.0, 1.0]], [[1.0, 1.0]], [[-1.0, -1.0]], [[0.0, 0.0]]]
   # make the x value structure of the NN by putting bias and initial value 0s.
   # for i in range(len(training_set)):
   #    for j in range(len(layer_counts)):
   #       if j == 0: x_vals[i][j].append(1.0)
   #       else: x_vals[i].append([0 for temp in range(layer_counts[j])])
   #print ('xv', x_vals) # [[[1.0, -1.0, 1.0], [0, 0], [0], [0]], [[-1.0, 1.0, 1.0], [0, 0], [0], [0]], ...

   # by using the layer counts, set initial weights [3, 2, 1, 1] => 3*2 + 2*1 + 1*1: Total 6, 2, and 1 weights are needed
   weights = [[round(random.uniform(-2.0, 2.0), 2) for j in range(layer_counts[i]*layer_counts[i+1])]  for i in range(len(layer_counts)-2)]
   weights.append([round(random.uniform(-2.0, 2.0), 2) for i in range(layer_counts[-1])])
   #weights = [[1.35, -1.34, -1.66, -0.55, -0.9, -0.58, -1.0, 1.78], [-1.08, -0.7], [-0.6]]   #Example 2
   print ('weights', weights)    #[[2.0274715389784507e-05, -3.9375970265443985, 2.4827119599531016, 0.00014994269071843774, -3.6634876683142332, -1.9655046461270405]
                        #[-3.7349985848630634, 3.5846029322774617]
                        #[2.98900741942973]]

   # build the structure of BP NN: E nodes and negative_gradients 
   E_vals = [[[*i] for i in j] for j in x_vals]  #copy elements from x_vals, E_vals has the same structures with x_vals
   negative_grad = [[*i] for i in weights]  #copy elements from weights, negative gradients has the same structures with weights
   errors = [10]*len(input)  # Whenever FF is done once, error will be updated. Start with 10 (a big num)
   count = 1  # count how many times you trained the network, this can be used for index calc or for decision making of 'restart'
   alpha = 0.3
   
   print('xv', x_vals)
   print('evals', E_vals)
   print('grad', negative_grad)
   print('errors', errors)

   
   # calculate the initail error sum. After each forward feeding (# of training sets), calculate the error and store at error list
   for k in range(len(input)):
      x_vals[k], errors[k] = ff(output[k], x_vals[k], weights, t_funct)
      #sum??
      #bp
      #modify weights
   err = sum(errors)
   #prev_err = err
   print("GEN", count, err, alpha)
   # print ('xv', x_vals)
   # print ('weights', weights)
   # print('evals', E_vals)
   # print('grad', negative_grad)
   # print('errors', errors)
   #reset = 0
   #print(err)

   while err > 0.01:# and count < 2:
      # if err > prev_err:
      #    alpha *= 0.5
      for k in range(len(input)):
         ng = bp(output[k], x_vals[k], weights, E_vals[k], negative_grad)[1]
         weights = update_weights(weights, ng, alpha)
      for k in range(len(input)):
         x_vals[k], errors[k] = ff(output[k], x_vals[k], weights, t_funct)
      #prev_err = err
      err = sum(errors)
      count += 1
      #print("GEN", count, err, alpha)
      #if (err > prev_err * 0.999 and err > 0.25) or (err > prev_err * 0.9999 and err < 0.25):
      if count % 5000 == 1 or err >= 2:
         weights = [[round(random.uniform(-2.0, 2.0), 2) for j in range(layer_counts[i]*layer_counts[i+1])]  for i in range(len(layer_counts)-2)]
         weights.append([round(random.uniform(-2.0, 2.0), 2) for i in range(layer_counts[-1])])
         # prev_err = err
         err = sum(errors)
         count += 1
        # print("GEN", count, err, alpha)
         #reset = count
         #alpha = 1
      # print ('xv', x_vals)
      # print ('weights', weights)
      # print('evals', E_vals)
      # print('grad', negative_grad)
      # print('errors', errors)
      
   ''' 
   while err is too big, reset all weights as random values and re-calculate the error sum.
   
   '''

   ''' 
   while err does not reach to the goal and count is not too big,
      update x_vals and errors by calling ff()
      whenever all training sets are forward fed, 
         check error sum and change alpha or reset weights if it's needed
      update E_vals and negative_grad by calling bp()
      update weights
      count++
   '''
   # print final weights of the working NN
   print('time', time.time() - start)
   print ('weights:')
   for w in weights: print (w)
if __name__ == '__main__': main()
# Taohan Lin, 7, 2024