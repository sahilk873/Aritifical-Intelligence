import math


def floyd(graph):
    numvertex = len(graph)
    for i in range(numvertex):
        for j in range(numvertex):
            for k in range(numvertex):
                graph[j][k] = min(graph[j][k], graph[j][i] + graph[i][k])
    for i in range(numvertex):
        print("\n")
        for j in range(numvertex):
            print(graph[i][j], end = " ")
    return ""



examplegraph = [[20, 50, 30, math.inf],
                [math.inf, 0, 15, 5],
                [30, math.inf, 0, 15],
                [15, 25, 5, 0]]


print(floyd(examplegraph))