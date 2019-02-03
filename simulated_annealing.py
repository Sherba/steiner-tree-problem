import random
from collections import deque

class SimulatedAnnealingSteiner:
    def __init__(self, graph, steiner_nodes):
        self.graph = graph                  # e.g. [(node1, node2, weight), ...]
        self.steiner_nodes = steiner_nodes  # list of steiner nodes
        self.current_best = None            # currently best tree
        self.current_fitness = 0            # fitnes of currenty best tree

        self.iterations = 0                 # iteration counter
        self.iterations_limit = 100         # limit for iterations ( exit condition )
        self.number_of_initial_trees = 3    # number of initial trees
        self.trim_iterations = 5            # number of cycles in `trim`

    def simulated_annealing(self):
        ''' Main function.

        return: tuple (int, int, int) containing best tree and its fitness
        '''
        self.initialize()

        while not self.condition():
            current_similar = self.trim(self.find_new_similar())
            fitness_similar = self.fitness(current_similar)
            if fitness_similar < self.current_fitness:
                self.current_fitness = current_similar
                self.current_fitness = fitness_similar
            self.iterations += 1
        
        return self.current_best, self.current_fitness 
    
    def is_valid(self, tree):
        ''' Checks if given tree is valid.

        param: tree - list of tuples [(int, int, int), ...]
        return: boolean
        '''
        if self.has_unused_steiner_nodes(tree) or self.has_cycle(tree):
            return False
        return True

    def has_cycle(self, tree):
        ''' Checks if given tree has cycle.

        param: tree - list of tuples [(int, int, int), ...]
        return: boolean
        '''
        if tree == []:
            return False
        start = tree[0][0]
        marked = []
        queue = deque([start])

        while len(queue) > 0:
            node = queue.popleft()
            if node in marked:
                return True 

            neighbours = [neighbour for neighbour in tree if neighbour[0] == node or neighbour[1] == node]
            
            for neighbour in neighbours:
                if neighbour not in marked:
                    queue.appendleft(neighbour)

            marked.append(node)
        return False

    def has_unused_steiner_nodes(self, tree):
        ''' Checks if given tree has unused steiner nodes.

        param: tree - list of tuples [(int, int, int), ...]
        return: boolean
        '''
        used_nodes = []
        for vertex in tree:
            used_nodes.append(vertex[0])
            used_nodes.append(vertex[1])
        used_nodes = list(set(used_nodes))

        for node in self.steiner_nodes:
            if node not in used_nodes:
                return True
        return False

    def condition(self):
        ''' Checks if main loop is supposed to end.

        return: boolean
        '''
        if self.iterations == self.iterations_limit:
            return True
        return False

    def initialize(self):
        ''' Creates `self.number_of_initial_trees` trees and chooses best of them to be `self.current_best`.
        
        return: None
        '''
        potential_trees = [self.create_initial_tree() for _ in range(self.number_of_initial_trees)]

        temp_tree = potential_trees[0]
        temp_fitness = self.fitness(temp_tree)

        for tree in potential_trees:
            tree_fitness = self.fitness(tree)
            if temp_fitness > tree_fitness:
                temp_tree = tree
                temp_fitness = tree_fitness
            
        self.current_best = temp_tree
        self.current_fitness = temp_fitness

    def create_initial_tree(self):
        ''' Creates one of trees for `initialize` function.

        return: tree - list of tuples [(int, int, int), ...]
        '''
        used_nodes = []
        used_nodes.append(self.steiner_nodes[0])
        initial_tree = []

        while self.has_unused_steiner_nodes(initial_tree):
            new_vertex = self.take_random_vertex(used_nodes)
            initial_tree.append(new_vertex)

            if self.has_cycle(initial_tree):
                initial_tree = [x for x in initial_tree if x != new_vertex]
            else:
                used_nodes.append(new_vertex[0])
                used_nodes.append(new_vertex[1])
                used_nodes = list(set(used_nodes))
        
        return self.trim(initial_tree)

    def take_random_vertex(self, used_nodes):
        ''' For given list of nodes returns random vertex that is next to one of them.

        param: used_nodes - list of ints
        return: vertex - tuple (int, int, int)
        '''
        neighbours = self.neighbours(used_nodes)
        return random.choice(neighbours)

    def neighbours(self, used_nodes):
        ''' For given list of nodes returns list of vertexes that are next to them.

        param: used_nodes - list of ints
        return: list of tuples [(int, int, int), ...] 
        '''
        retval = []
        for vertex in self.graph:
            if vertex[0] in used_nodes or vertex[1] in used_nodes:
                retval.append(vertex)
        return retval
            
    def find_new_similar(self):
        ''' For current best tree finds tree similar to it.

        return: tree - list of tuples [(int, int, int), ...]
        '''
        old_tree = [vertex for vertex in self.current_best]
        victim_vertex = random.choice(old_tree)

        node1 = victim_vertex[0]
        node2 = victim_vertex[1]

        unused_nodes = self.unused_nodes(old_tree)
        if len(unused_nodes) == 0:
            return self.current_best
        bridge_node = random.choice(unused_nodes)

        new_tree = [x for x in old_tree if x != victim_vertex]
        
        bridge1 = self.find_vertex(node1, bridge_node)
        bridge2 = self.find_vertex(node2, bridge_node)

        new_tree.append(bridge1)        
        new_tree.append(bridge2)

        return new_tree

    def find_vertex(self, node1, node2):
        ''' For two given nodes finds vertex between them.

        return: tuple (int, int, int)
        '''
        return [
            vertex for vertex in self.graph if 
                (vertex[0] == node1 and vertex[1] == node2)
                or
                (vertex[0] == node2 and vertex[1] == node1)
        ][0]

    def unused_nodes(self, tree):
        ''' For given tree finds unused nodes.

        return: list[int]
        '''

        used_nodes = []
        for vertex in tree:
            used_nodes.append(vertex[0])
            used_nodes.append(vertex[1])
        used_nodes = list(set(used_nodes))

        all_nodes = []
        for vertex in self.graph:
            all_nodes.append(vertex[0])
            all_nodes.append(vertex[1])
        all_nodes = list(set(all_nodes))

        retval = [node for node in all_nodes if node not in used_nodes]
        return retval

    def fitness(self, tree):
        ''' Returns weight of given tree.

        param: tree - list of tuples [(int, int, int), ...]
        return: int
        '''
        return sum(weight for _, _, weight in tree)

    def trim(self, tree):
        ''' Returns tree without some unnecessary vertexes.

        param: tree - list of tuples [(int, int, int), ...]
        return: tree - list of tuples [(int, int, int), ...]
        '''
        new_tree = [vertex for vertex in tree]
        for _ in range(self.trim_iterations):
            node_dict = {}
            for vertex in new_tree:
                node1 = vertex[0]
                node2 = vertex[1]

                if node1 in node_dict:
                    node_dict[node1] += 1
                else:
                    node_dict[node1] = 1

                if node2 in node_dict:
                    node_dict[node2] += 1
                else:
                    node_dict[node2] = 1
            
            excess_vertexes = [
                vertex for vertex in new_tree 
                    if (node_dict[vertex[0]] == 1 and vertex[0] not in self.steiner_nodes) 
                        or (node_dict[vertex[1]] == 1 and vertex[1] not in self.steiner_nodes)
            ]
            if len(excess_vertexes) == 0:
                break

            new_tree = [vertex for vertex in tree if vertex not in excess_vertexes]
        
        return new_tree
