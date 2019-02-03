from simulated_annealing import SimulatedAnnealingSteiner

def make_simple_graph(n, w):
     return [(a, b, w) for a in range(n) for b in range(n) if a < b]
 
if __name__ == "__main__":
    solver = SimulatedAnnealingSteiner(make_simple_graph(15, 1), [1, 3, 4, 5, 6, 12])
    print( solver.simulated_annealing() )