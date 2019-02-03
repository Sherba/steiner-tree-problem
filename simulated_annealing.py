import random
from collections import deque

class SimulatedAnnealingSteiner:
    def __init__(self, graph, steiner_nodes):
        self.graph = graph  # e.g. [(node1, node2, weight), ...]
        self.steiner_nodes = steiner_nodes
        self.current_best = None
        self.current_fitness = 0

        # metadata:
        self.iterations = 0
        self.iterations_limit = 100
        self.initial_tree_size = 3

    def simulated_annealing(self):
        self.initialize()

        while not self.condition():
            current_similar = self.trim(self.find_new_similar())
            fitness_similar = self.fitness(current_similar)
            if fitness_similar < self.current_fitness:
                self.current_fitness = current_similar
                self.current_fitness = fitness_similar
                # TODO: add trim function maybe?
            self.iterations += 1
        
        return self.current_best, self.current_fitness 
    
    def is_valid(self, tree):
        if self.has_unused_steiner_nodes(tree) or self.has_cycle(tree):
            return False
        return True

    def has_cycle(self, tree):
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
        if self.iterations == self.iterations_limit:
            return True
        return False

    def initialize(self):
        potential_trees = [self.create_initial_tree() for _ in range(self.initial_tree_size)]

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
        used_nodes = []
        used_nodes.append(self.steiner_nodes[0])
        initial_tree = []

        while self.has_unused_steiner_nodes(initial_tree):
            new_vertex = self.take_random_vertex(used_nodes)
            initial_tree.append(new_vertex)
            if self.has_cycle(initial_tree):
                initial_tree = [x for x in initial_tree if x != new_vertex]
        
        return self.trim(initial_tree)

    def take_random_vertex(self, used_nodes):
        neighbours = self.neighbours(used_nodes)
        return random.choice(neighbours)

    def neighbours(self, used_nodes):
        retval = []
        for vertex in self.graph:
            if vertex[0] in used_nodes or vertex[1] in used_nodes:
                retval.append(vertex)
        return retval
            
    # finds similar to current best
    def find_new_similar(self):
        old_tree = [vertex for vertex in self.current_best]
        victim_vertex = random.choice(old_tree)

        node1 = victim_vertex[0]
        node2 = victim_vertex[1]

        unused_nodes = self.unused_nodes(old_tree)
        bridge_node = random.choice(unused_nodes)

        new_tree = [x for x in old_tree if x != victim_vertex]
        
        bridge1 = self.find_vertex(node1, bridge_node)
        bridge2 = self.find_vertex(node2, bridge_node)

        new_tree.append(bridge1)        
        new_tree.append(bridge2)

        return new_tree

    def find_vertex(self, node1, node2):
        return [
            vertex for vertex in self.graph if 
                (vertex[0] == node1 and vertex[1] == node2)
                or
                (vertex[0] == node2 and vertex[1] == node1)
        ][0]

    def unused_nodes(self, tree):
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
        return sum(weight for _, _, weight in tree)

    def trim(self, tree):
        new_tree = [vertex for vertex in tree]
        while True:
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
