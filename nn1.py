#import sys; args = sys.argv[1:]
args = ['weights.txt', 'T3', '0', '0', '0']


import math

def transfer(t_funct, input):
   sumfunction = sum(input)
   if t_funct == 'T1':
      return sumfunction
   elif t_funct == 'T2':
      if sumfunction <= 0:
         return 0
      else:
         return 1 
   elif t_funct == 'T3':
      return 1 / (1 + math.e**(-sumfunction))
   elif t_funct == 'T4':
      return -1 + 2 / (1 + math.e**(-sumfunction))
   else:
      return None

def dot_product(input_vals, weights, layer):
   result = []
   cell = 0
   while cell < len(weights[layer]):
      output = []
      weight = 0
      while weight < len(weights[layer][cell]):
         output.append(input_vals[weight] * weights[layer][cell][weight])
         weight += 1
      result.append(output)
      cell += 1
   return result
       

def evaluate(args, input_vals, t_funct):
   initial = input_vals
   with open(args[0]) as weightfile:
        layerweights = []
        for weightlist in weightfile:
           weightlist = list(weightlist) #next three lines only for testing future nns
           weightlist.pop(0)
           weightlist = "".join(weightlist)
           layerweights.append([float(k) for k in weightlist.strip().split(', ')])
   weights = []
   for term in layerweights:
      print(len(term))
   inputcount = len(input_vals)
   for i in range(len(layerweights)):
      cw = []
      for cell in range(len(layerweights[i]) // inputcount + 1):
         nextcell = cell + 1
         cw.append(layerweights[i][cell*inputcount:(nextcell)*inputcount])
      weights.append(cw)
      inputcount = len(cw)
   for layer in range(len(weights) - 1):
      weighted_input = dot_product(initial, weights, layer)
      initial = []
      for input_val in weighted_input:
         initial.append(transfer(t_funct, input_val))
   output = []
   for neuron in range(len(weights[len(weights) - 1][0])):
        output.append(weights[len(weights)-1][0][neuron] * initial[neuron])
   cleaned = []
   for term in output:
      if term != -0.0:
         cleaned.append(term)
      if term == -0.0:
         cleaned.append(0.0)
   return cleaned
    
def main():
   inputs, t_funct, transfer_found = [], 'T1', False
   for arg in args[1:]:
      if not transfer_found:
         t_funct, transfer_found = arg, True
      else:
         inputs.append(float(arg))
   li =(evaluate(args, inputs, t_funct)) #ff
   for x in li:
      print (x, end=' ') # final outputs
if __name__ == '__main__': main()
# Sahil Kapadia, Period 7, 2024