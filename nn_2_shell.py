import sys; args = sys.argv[1:]
infile = open(args[0])
import math, random

# t_funct is symbol of transfer functions: 'T1', 'T2', 'T3', or 'T4'
# input is a list of input (summation) values of the current layer
# returns a list of output values of the current layer
def transfer(t_funct, input):
   if t_funct == 'T3': return [1 / (1 + math.e**-x) for x in input]
   elif t_funct == 'T4': return [-1+2/(1+math.e**-x) for x in input]
   elif t_funct == 'T2': return [x if x > 0 else 0 for x in input]
   else: return [x for x in input]

# returns a list of dot_product result. the len of the list == stage
# dot_product([x1, x2, x3], [w11, w21, w31, w12, w22, w32], 2) => [x1*w11 + x2*w21 + x3*w31, x1*w12, x2*w22, x3*w32] 
def dot_product(input, weights, stage):
   return [sum([input[x]*weights[stage][s*len(input)+x] for x in range(len(input))]) for s in range(int(len(weights[stage])/len(input)))]

# Complete the whole forward feeding for one input(training) set
# return updated x_vals and error of the one forward feeding
def ff(ts, xv, weights, t_funct):
   ''' ff coding goes here '''
   for i in range(len(weights)-1):
      temp=dot_product(xv[i], weights, i)
      for j in range(len(temp)):
         xv[i+1][j]=temp[j]
      xv[i+1]=transfer(t_funct, xv[i+1])
   for i in range(len(xv[-1])):
      xv[-1][i]=xv[-2][i]*weights[-1][i]

   err = sum([(ts[i-len(xv[-1])] - xv[-1][i])**2 for i in range(len(xv[-1]))]) / 2
   return xv, err

# Complete the back propagation with one training set and corresponding x_vals and weights
# update E_vals (ev) and negative_grad, and then return those two lists
def bp(ts, xv, weights, ev, negative_grad):  
   for j in range(len(weights[-1])):
         ev[-1][j]=ts[-len(weights[-1])+j]-xv[-1][j]
   for i in range(len(xv)-2):
      ind=len(xv)-i-2
      for j in range(len(xv[ind])):
         ev[ind][j]=xv[ind][j]*(1-xv[ind][j])*(sum([ev[ind+1][k]*weights[ind][j+k*len(ev[ind+1])] for k in range(len(ev[ind+1]))]))
         for k in range(len(xv[ind+1])):
            negative_grad[ind][k*len(xv[ind+1])+j]=ev[ind+1][k]*xv[ind][j]

   for i in range(len(negative_grad[0])):
      negative_grad[0][i]=ts[i%len(ts)]*ev[1][i//len(ts)]

   return ev, negative_grad

# update all weights and return the new weights
# Challenge: one line solution is possible
def update_weights(weights, negative_grad, alpha):
   for i in range(len(weights)):
      for j in range(len(weights[i])):
         weights[i][j]=negative_grad[i][j]*alpha+weights[i][j]
   return weights

def evaluate(file):
   lines=[]
   f=file.read().split('\n')
   for i in f:
      temp=i.split()
      line=[]
      count=0
      layer_count=[]
      for j in temp:
         if j!="=>":
            count+=1
            line.append(float(j))
         else:
            layer_count.append(count+1)
            count=0
      layer_count.append(count+1)
      if (len(line)!=0):
         lines.append(line)
   layer_count.append(layer_count[1]-1)
   layer_count.append(layer_count[1]-1)
   return lines, layer_count

def main():
   t_funct = 'T3' # we default the transfer(activation) function as 1 / (1 + math.e**(-x))
   ''' work on training_set and layer_count '''
   training_set, layer_counts = evaluate(infile)  # list of lists
   #print (training_set) #[[1.0, -1.0, 1.0], [-1.0, 1.0, 1.0], [1.0, 1.0, 1.0], [-1.0, -1.0, 1.0], [0.0, 0.0, 0.0]]
   #layer_counts = [] # set the number of layers: (# of input + 1), (# of output + 1), # of output, # of output
   print ('layer counts', layer_counts) # This is the first output. [3, 2, 1, 1] with teh given x_gate.txt

   ''' build NN: x nodes and weights '''
   x_vals = [[temp[0:len(temp)-1]] for temp in training_set] # x_vals starts with first input values
   #print (x_vals) # [[[1.0, -1.0]], [[-1.0, 1.0]], [[1.0, 1.0]], [[-1.0, -1.0]], [[0.0, 0.0]]]
   # make the x value structure of the NN by putting bias and initial value 0s.
   for i in range(len(training_set)):
      for j in range(len(layer_counts)):
         if j == 0: x_vals[i][j].append(1.0)
         else: x_vals[i].append([0 for temp in range(layer_counts[j])])
   #print (x_vals) # [[[1.0, -1.0, 1.0], [0, 0], [0], [0]], [[-1.0, 1.0, 1.0], [0, 0], [0], [0]], ...


   # by using the layer counts, set initial weights [3, 2, 1, 1] => 3*2 + 2*1 + 1*1: Total 6, 2, and 1 weights are needed
   weights = [[round(random.uniform(-2.0, 2.0), 2) for j in range(layer_counts[i]*layer_counts[i+1])]  for i in range(len(layer_counts)-2)]
   weights.append([round(random.uniform(-2.0, 2.0), 2) for i in range(layer_counts[-1])])
   #weights = [[1.35, -1.34, -1.66, -0.55, -0.9, -0.58, -1.0, 1.78], [-1.08, -0.7], [-0.6]]   #Example 2
   # print (weights)    #[[2.0274715389784507e-05, -3.9375970265443985, 2.4827119599531016, 0.00014994269071843774, -3.6634876683142332, -1.9655046461270405]
                        #[-3.7349985848630634, 3.5846029322774617]
                        #[2.98900741942973]]2
   #weights=[[-1.48, 0.9, -1.11, 1.02, -0.64, -1.2, -1.54, -0.05], [1.8, -1.61], [0.32]]
   # build the structure of BP NN: E nodes and negative_gradients 
   E_vals = [[[*i] for i in j] for j in x_vals]  #copy elements from x_vals, E_vals has the same structures with x_vals
   negative_grad = [[*i] for i in weights]  #copy elements from weights, negative gradients has the same structures with weights
   errors = [10]*len(training_set)  # Whenever FF is done once, error will be updated. Start with 10 (a big num)
   count = 1  # count how many times you trained the network, this can be used for index calc or for decision making of 'restart'
   alpha = 0.5
   err = sum(errors)
   check=1
   initial_error=0
   #weights=[weights]*len(training_set)
   #print (weights)
   # calculate the initial error sum. After each forward feeding (# of training sets), calculate the error and store at error list
   
   while (err>0.01):
      for k in range(len(training_set)):
         #print (weights)
         x_vals[k], errors[k] = ff(training_set[k], x_vals[k], weights, t_funct)
         #print (x_vals[k])
         #print (x_vals[k], errors[k])
         #sum??
         #bp
         E_vals[k], negative_grad= bp(training_set[k], x_vals[k], weights, E_vals[k], negative_grad)
         #print (E_vals[k])
         #print (negative_grad)
         weights=update_weights(weights, negative_grad, alpha)
         #print (weights)
      count+=1
      check+=1
      err = sum(errors)
      if (check==2):
         initial_error=err
      print (errors)
      print (count, err)
      if (check==1000 and err>initial_error):
         check=1
         weights = [[round(random.uniform(-2.0, 2.0), 2) for j in range(layer_counts[i]*layer_counts[i+1])]  for i in range(len(layer_counts)-2)]
         weights.append([round(random.uniform(-2.0, 2.0), 2) for i in range(layer_counts[-1])])
      if (check>3000 and (err>0.1 or abs(initial_error-err)<0.1)):
         check=1
         weights = [[round(random.uniform(-2.0, 2.0), 2) for j in range(layer_counts[i]*layer_counts[i+1])]  for i in range(len(layer_counts)-2)]
         weights.append([round(random.uniform(-2.0, 2.0), 2) for i in range(layer_counts[-1])])
   
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
   print ('weights:')
   for w in weights: print (w)
if __name__ == '__main__': main()
# Michelle Kang, 7, 2024