from strassen import *
from random import uniform
import csv


# def generate_graph(prob):
   # prob = 1-prob
   #g = [[1 if uniform(0, 1) >= prob else 0 for j in range(1024)] for i in range(1024)]
   # return g 
def generate_graph(probability):
    probability = 1 - probability
    graph = []
    for i in range(1024):
        row = []
        for j in range(1024):
            if uniform(0, 1) >= probability:
                row.append(1)
            else:
                row.append(0)
        graph.append(row)
    return graph

#outfile = open("results.csv", "w")
#for p in [0.01, 0.02, 0.03, 0.04, 0.05]:
#    for t in range(5):
 #       g = generate_graph(p)
  #      a2 = strassens(g, g, crossover=128)
   #     a3 = strassens(g, a2, crossover=128)
    ##
      #  line = "{},{}".format(p, triangles)
       # outfile.write(line + "\n")
        #outfile.flush()
        #print(p, triangles)
#outfile.close()



with open("results.csv", "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Probability', 'Triangles'])

    for probability in [0.01, 0.02, 0.03, 0.04, 0.05]:
        for t in range(5):
            graph = generate_graph(probability)
            matrix_1 = strassens(graph, graph, crossover=128)
            matrix_2 = strassens(graph, matrix_1, crossover=128)
            triangles = sum([matrix_2[i][i] for i in range(len(matrix_2))])/6

            writer.writerow([probability, triangles])
            print(probability, triangles)