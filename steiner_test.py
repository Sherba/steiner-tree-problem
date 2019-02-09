from simulated_annealing import SimulatedAnnealingSteiner
from random import randint
from statistics import mean

def make_simple_graph(n):
     return [(a, b, 1) for a in range(n) for b in range(n) if a < b]

if __name__ == "__main__":
    a = []

    n = 25
    nodes = [1, 3, 6, 9, 11, 12, 13, 14]
    number_nodes = len(nodes)

    solver = SimulatedAnnealingSteiner(make_simple_graph(n), nodes)

    for _ in range(50):
        result = solver.simulated_annealing()    
        a.append(result[1])

    print("[ {}: {} ]".format(n, number_nodes))
    print(a)
    print(min(a))
    print(mean(a))
