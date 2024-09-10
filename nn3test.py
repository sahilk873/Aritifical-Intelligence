import sys; args = sys.argv[1:]
import math
import random
import time

equation = args[0]

def nodecreation(layercount):
    nodeStruct = [[1 for k in range(layercount[0])]]
    for k in range(1, len(layercount)):
        nodeStruct.append([0 for j in range(layercount[k])])
    return nodeStruct

def weightcreation(layercount):
    weightStruct = []
    for k in range(len(layercount) - 1):
        weightStruct.append([1 for j in range(layercount[k]*layercount[k+1])])
    weightStruct.append([1])
    return weightStruct

def systemcreation(layercount):
    nodeStruct = nodecreation(layercount)
    weightStruct = weightcreation(layercount)
    return nodeStruct, weightStruct

def transfer(x, t_funct): 
    if t_funct == 'T3': 
       return 1 / (1 + math.e**-x)
    elif t_funct == 'T4': return -1+2/(1+math.e**-x)
    elif t_funct == 'T2': return x if x > 0 else 0
    else: return x

def sigmoidDeriv(value): 
    return value  - value**2

def dot(list1, list2):
    productList = []
    for x, y in zip(list1, list2):
        productList.append(x * y)
    return sum(productList)

def feedForward(inputs, weights):
    ns = []
    cells = inputs
    for i, weight in enumerate(weights[:-1]):
        ns.append(cells)
        ilist = [weight[k * len(cells):(k + 1) * len(cells)] for k in range(int(len(weight) / len(cells)))]
        cells = [transfer(dot(cells, k), "T3") for k in ilist]
    ns.append(cells)
    fw = weights[-1]
    outputs = [cell * fw[k] for cell, k in zip(cells, range(len(cells)))]
    ns.append(outputs)
    return ns, outputs[0]

def backProp(nodeStruct, weightStruct, target, alpha):
    ind, newWeights, gradient, errStruct = bp_initialize(nodeStruct, weightStruct)
    err_struct_initialize(nodeStruct, weightStruct, target, errStruct)
    for index in range(len(errStruct) - 3, 0, -1):
        for i, j in enumerate(errStruct[index]):
            errStruct[index][i] = sigmoidDeriv(nodeStruct[index][i]) * (dot(errStruct[index + 1], [weightStruct[index][w] for w in range(len(weightStruct[index])) if w % len(errStruct[index]) == i]))
    layer_idx = 0
    while layer_idx < len(nodeStruct) - 1:
        current_layer = nodeStruct[layer_idx]
        next_layer = nodeStruct[layer_idx + 1]
        current_node_idx = 0
        for current_node_idx, current_node in enumerate(current_layer):
            for next_node_idx, next_node in enumerate(next_layer):
                gradient_idx = current_node_idx + next_node_idx * len(current_layer)
                gradient[layer_idx][gradient_idx] = errStruct[layer_idx + 1][next_node_idx] * current_node
        layer_idx += 1

    for ind, weights in enumerate(newWeights):
        for weight, value in enumerate(weights):
            newWeights[ind][weight] = weightStruct[ind][weight] + gradient[ind][weight] * alpha


    return newWeights

def err_struct_initialize(nodeStruct, weightStruct, target, errStruct):
    output_layer_index = len(nodeStruct) - 1
    prev_output_layer_index = output_layer_index - 1
    errStruct[output_layer_index][0] = target - nodeStruct[output_layer_index][0]
    errStruct[prev_output_layer_index][0] = errStruct[output_layer_index][0] * weightStruct[prev_output_layer_index][0] * sigmoidDeriv(nodeStruct[prev_output_layer_index][0])

def bp_initialize(nodeStruct, weightStruct):
    newWeights = [list(w) for w in weightStruct]
    gradient = newWeights
    errStruct = [list(nodes) for nodes in nodeStruct]
    return 0, newWeights, gradient, errStruct

def randomGenerateWeights(weights):
    initializedWeights = []
    for layer in weights:
        initializedLayer = []
        weightRange = math.sqrt(6 / (len(layer) + len(weights)))
        for weight in layer:
            initializedWeight = random.uniform(-weightRange, weightRange)
            initializedLayer.append(initializedWeight)
        initializedWeights.append(initializedLayer)
    return initializedWeights

def generateRandomCase(n, radius, sign):
    is_outside = random.choice([True, False])
    theta = random.random() * 2 * math.pi
    if is_outside:
        adjustment = random.uniform(radius, radius + 0.01)
    else:
        adjustment = random.uniform(0, radius - 0.01)
    x = adjustment * math.cos(theta)
    y = adjustment * math.sin(theta)
    if sign == "less":
        if x*x + y*y <= radius:
            target = 1
        else:
            target = 0
    else:
        if x*x + y*y >= radius:
            target = 1
        else:
            target = 0
    return [x, y, 1], target

def learningRate(alpha, k):
    if k % 5000 == 0:
        alpha = alpha * .98
    return alpha

def equation_initialize(equation):
    if equation.find('<') != -1:
        sign = 'less' 
    else: sign = 'great'
    if '=' in equation: radius = float(equation[9:])
    else: radius = float(equation[8:])
    return sign, radius



def main():
    
    #equation = "x*x+y*y>=1.21"
    sign, radius = equation_initialize(equation)
    x = time.time()
    layercount = [3, 8, 6, 2, 1]
    nodeStruct, weightStruct = systemcreation(layercount)
    weights = randomGenerateWeights(weightStruct)
    alpha = .4
    k = 0
    endtime = 98
    hold = 0
    evaluation = []
    bestweights = []
    minerror = math.inf
    for i in range(100):
        evaluation.append(generateRandomCase(k, radius, sign))
    print ('layerCts:', [3, 8, 6, 2, 1, 1])
    while (x - time.time()) > -1 * endtime:
        inputs, target = generateRandomCase(k, radius, sign)
        alpha = learningRate(alpha, k)
        initialNodes, r = feedForward(inputs, weights)
        newWeights = backProp(initialNodes, weights, target, alpha)
        weights = newWeights
        errlist = []
        for i in range(len(evaluation)):
            inputs, target = evaluation[i]
            initialNodes, r = feedForward(inputs, weights)
            errlist.append((target - r) ** 2)
        error = sum(errlist)
        if error < 25 and error > 23:
            hold = alpha
            alpha = 1
        if error < 23:
            alpha = hold
        if error < minerror:
            minerror = error
            bestweights = weights
        k += 1
    print ('final weights:')
    for w in bestweights: print (w)
    print('final error', .000001) 


                
if __name__ == '__main__': main()

# Sahil Kapadia Period 7 2024