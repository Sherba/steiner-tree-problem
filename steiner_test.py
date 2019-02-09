from simulated_annealing import SimulatedAnnealingSteiner
from random import randint
from statistics import mean

def make_simple_graph(n):
     return [(a, b, 1) for a in range(n) for b in range(n) if a < b]

if __name__ == "__main__":
    a = []
    n = 10
    number_of_steiner = 4
    solver = SimulatedAnnealingSteiner(make_simple_graph(n), [1, 3, 6, 9])

    for _ in range(150):
        result = solver.simulated_annealing()    
        a.append(result[1])
        # if result is imposible print the tree
        if result[1] < number_of_steiner-1:
            print(result[0])
        # print( solver.simulated_annealing() )

    print("Dobijene vrednosti za {} cvorova i {} stajnerova cvora".format(n, number_of_steiner))
    print(a)
    print(min(a))
    print(mean(a))

# Mali tester za testiranje algoritma nad razlicitim grafovima
