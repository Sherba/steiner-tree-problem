from simulated_annealing import SimulatedAnnealingSteiner
from random import randint
from statistics import mean

def make_simple_graph(n):
     return [(a, b, 1) for a in range(n) for b in range(n) if a < b]

if __name__ == "__main__":
    a = []
    n = 20
    number_of_steiner = 7
    for _ in range(30):
        solver = SimulatedAnnealingSteiner(make_simple_graph(n), [1, 4, 7, 8, 11, 14,18])
        a.append(solver.simulated_annealing()[1])
        # print( solver.simulated_annealing() )

    print("Dobijene vrednosti za {} cvorova i {} stajnerova cvora".format(n, number_of_steiner))
    print(a)
    print(min(a))
    print(mean(a))

# Mali tester za testiranje algoritma nad razlicitim grafovima
