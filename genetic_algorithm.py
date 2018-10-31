# Valentin Macé
# valentin.mace@kedgebs.com
# Developed for fun
# Feel free to use this code as you wish as long as you quote me as author

"""
genetic_algorithm.py
~~~~~~~~~~

A module to implement a genetic algorithm to train neural networks playing snake game.
The parent selection is done through tournament, crossover and mutation
can operate on individual weights, neurons or even whole layer.

Note:
  - This is one implementation that worked for me but might be far from optimum.
  - I only parallelize part of the code in order to let the CPU cool down during long training sessions
"""

import copy
import multiprocessing
from random import randint
from game import*
from neural_network import *
from joblib import Parallel, delayed


class GeneticAlgorithm:
    """ Genetic Algorithm Class """

    def __init__(self, networks=None, networks_shape=None, population_size=1000, generation_number = 100,
                 crossover_rate=0.3, crossover_method='neuron', mutation_rate=0.7, mutation_method='weight'):
        """
        :param networks(list of NeuralNetwork): First generation networks
        :param networks_shape(list of int): List defining number of layers and number of neurons in each layer
        :param population_size(int): Number of networks for each generation
        :param generation_number(int): How many generation the algorithm will run on
        :param crossover_rate(int): Proportion of children to be produced at each generation
        :param crossover_method(str): How children will be produced
        :param mutation_rate(int): Proportion of the population to mutate at each generation
        :param mutation_method(str): How mutation will be done
        """
        self.networks_shape = networks_shape
        if self.networks_shape is None:             # if no shape is provided
            self.networks_shape = [21,16,3]         # default shape
        self.networks = networks

        if networks is None:                                  # if no networks are provided
            self.networks = []
            for i in range(population_size):                  # producing population
                self.networks.append(NeuralNetwork(self.networks_shape))

        self.population_size = population_size
        self.generation_number = generation_number
        self.crossover_rate = crossover_rate
        self.crossover_method = crossover_method
        self.mutation_rate = mutation_rate
        self.mutation_method = mutation_method

    def start(self):
        """
        Main function operating the Genetic Algorithm, some steps are parallelized

        Steps at each generation:
        1- Parents selection
        2- Offsprings production
        3- Mutated individuals production
        4- Evaluation of whole population (old population + offsprings + mutated individuals)
        5- Additional mutations on random individuals (seems to improve learning)
        6- Keeping only *population_size* individuals, throwing bad performers

        :return: Nothing
        """
        networks = self.networks
        population_size = self.population_size
        crossover_number = int(self.crossover_rate*self.population_size)   # calculate number of children to be produced
        mutation_number = int(self.mutation_rate*self.population_size)     # calculate number of mutation to be done

        num_cores = multiprocessing.cpu_count()         # number of cores in your computer for later parallelization
        gen = 0                                         # current generation
        for i in range(self.generation_number):
            gen += 1

            parents = self.parent_selection(networks, crossover_number, population_size)       # parent selection
            children = self.children_production(crossover_number, parents)                     # children making
            mutations = self.mutation_production(networks, mutation_number, population_size)   # mutations making

            networks = networks + children + mutations                      # old population and new individuals
            self.evaluation(networks, num_cores)                            # evaluation of neural nets
            networks.sort(key=lambda Network: Network.score, reverse=True)  # ranking neural nets
            networks[0].save(name="gen_"+str(gen))                          # saving best of current generation

            for i in range(int(0.2*len(networks))):              # More random mutations because it helps
                rand = randint(10, len(networks)-1)
                networks[rand] = self.mutation(networks[rand])

            networks = networks[:population_size]       # Keeping only best individuals
            self.print_generation(networks, gen)

    def parent_selection(self, networks, crossover_number, population_size):
        """
        Parent selection function, takes 3 random individuals and makes a tournament between them,
        the winner is selected as a parent

        :param networks: list of neural nets
        :param crossover_number: number of parents needed
        :param population_size: well..
        :return: list of selected parents
        """
        parents = []
        for i in range(crossover_number):
            parent = self.tournament(networks[randint(0, population_size - 1)],      # running tournament
                                     networks[randint(0, population_size - 1)],
                                     networks[randint(0, population_size - 1)])
            parents.append(parent)                                                   # append selected parent
        return parents

    def children_production(self, crossover_number, parents):
        """
        Takes randomly 2 parents in the parents list and makes them crossover to give a child
        Note: the crossover method is contained in self.crossover_method

        :param crossover_number: number of children needed
        :param parents: list of parents
        :return: list of made up children
        """
        children = []
        for i in range(crossover_number):
            child = self.crossover(parents[randint(0, crossover_number - 1)],       # child making
                                   parents[randint(0, crossover_number - 1)])
            children.append(child)                                                  # append child
        return children

    def mutation_production(self, networks, mutation_number, population_size):
        """
        Makes new individuals from individuals in the current population by mutating them
        Note: it does not affect current individuals but actually creates new ones

        :param networks: list of neural nets
        :param mutation_number: number of mutants needed
        :param population_size: size of.. you know..
        :return: list of new individuals (mutants)
        """
        mutations = []
        for i in range(mutation_number):
            mut = self.mutation(networks[randint(0, population_size - 1)])      # mutant making
            mutations.append(mut)                                               # append mutant
        return mutations

    def evaluation(self, networks, num_cores, ):
        """
        Takes the population of neural nets and makes them play 4 games each, a neural_net score is the mean
        of its 4 games
        Note: the 4 games are run in parallel using Joblib

        :param networks: list of neural nets
        :param num_cores: Number of cores of your computer
        :return: Nothing but each neural_net in networks is now evaluated (in neural_net.score)
        """
        game = Game()
        results1 = Parallel(n_jobs=num_cores)(delayed(game.start)(neural_net=networks[i]) for i in range(len(networks)))
        results2 = Parallel(n_jobs=num_cores)(delayed(game.start)(neural_net=networks[i]) for i in range(len(networks)))
        results3 = Parallel(n_jobs=num_cores)(delayed(game.start)(neural_net=networks[i]) for i in range(len(networks)))
        results4 = Parallel(n_jobs=num_cores)(delayed(game.start)(neural_net=networks[i]) for i in range(len(networks)))
        for i in range(len(results1)):
            networks[i].score = int(np.mean([results1[i], results2[i], results3[i], results4[i]]))

    def tournament(self, net1, net2, net3):
        """
        Takes 3 neural nets, makes them play a game each and select the best performer

        :param net1: neural net (1st participant)
        :param net2: neural net (2nd participant)
        :param net3: last but not least, the third contender
        :return: the winning neural net
        """
        game = Game()
        game.start(neural_net=net1)                # net1 plays a game and so on..
        score1 = game.game_score
        game.start(neural_net=net2)
        score2 = game.game_score
        game.start(neural_net=net3)
        score3 = game.game_score
        maxscore = max(score1, score2, score3)     # the best one is returned
        if maxscore == score1:
            return net1
        elif maxscore == score2:
            return net2
        else:
            return net3

    def crossover(self, net1, net2):
        """
        Takes two neural nets and produce a child according to the method contained in
        self.crossover_method

        Example of working (method = 'neuron'):
        1- Two networks are created (copies of each parent)
        2- Selects a random neuron in a random layer OR a random bias in a random layer
        3- Switches this neuron OR bias between the two networks
        4- Each network plays a game
        5- Best one is selected
        Principle is the same for weight or layer methods

        :param net1: neural net (first parent)
        :param net2: neural net (second parent)
        :return: neural net (child)
        """
        res1 = copy.deepcopy(net1)                 # making copies (children) otherwise we manipulate the actual parents
        res2 = copy.deepcopy(net2)
        weights_or_biases = random.randint(0, 1)   # choosing randomly if crossover is over bias or weight/neuron/layer
        if weights_or_biases == 0:                 # crossover over weight/neuron/layer
            if self.crossover_method == 'weight':
                layer = random.randint(0, len(res1.weights) - 1)                            # random layer
                neuron = random.randint(0, len(res1.weights[layer]) - 1)                    # random neuron
                weight = random.randint(0, len(res1.weights[layer][neuron]) - 1)            # random weight
                temp = res1.weights[layer][neuron][weight]                                  # switching weights
                res1.weights[layer][neuron][weight] = res2.weights[layer][neuron][weight]
                res2.weights[layer][neuron][weight] = temp
            elif self.crossover_method == 'neuron':
                layer = random.randint(0, len(res1.weights) - 1)                            # random layer
                neuron = random.randint(0, len(res1.weights[layer]) - 1)                    # random neuron
                temp = copy.deepcopy(res1)                                                  # switching neurons
                res1.weights[layer][neuron] = res2.weights[layer][neuron]
                res2.weights[layer][neuron] = temp.weights[layer][neuron]
            elif self.crossover_method == 'layer':
                layer = random.randint(0, len(res1.weights) - 1)                            # random layer
                temp = copy.deepcopy(res1)                                                  # switching layers
                res1.weights[layer] = res2.weights[layer]
                res2.weights[layer] = temp.weights[layer]
        else:                                                       # crossover over bias
            layer = random.randint(0, len(res1.biases) - 1)         # random layer
            bias = random.randint(0, len(res1.biases[layer]) - 1)   # random bias
            temp = copy.deepcopy(res1)                              # switching biases
            res1.biases[layer][bias] = res2.biases[layer][bias]
            res2.biases[layer][bias] = temp.biases[layer][bias]

        game = Game()
        game.start(neural_net=res1)     # child 1 plays a game
        score1 = game.game_score
        game.start(neural_net=res2)     # child 2 plays a game
        score2 = game.game_score
        if score1 > score2:             # returns best one
            return res1
        else:
            return res2

    def mutation(self, net):
        """
        Takes a neural net and makes a clone with a mutation according to the method contained in
        self.mutation_method

        :param net: neural network that will be cloned
        :return: neural network similar to the net param except where the mutation occurred
        """
        res = copy.deepcopy(net)                    # making copy otherwise we manipulate the actual net in params
        weights_or_biases = random.randint(0, 1)    # choosing randomly if mutation is over bias or weight/neuron
        if weights_or_biases == 0:                  # mutation over weight/neuron
            if self.mutation_method == 'weight':
                layer = random.randint(0, len(res.weights) - 1)                  # random layer
                neuron = random.randint(0, len(res.weights[layer]) - 1)          # random neuron
                weight = random.randint(0, len(res.weights[layer][neuron]) - 1)  # random weight
                res.weights[layer][neuron][weight] = np.random.randn()           # mutation
            elif self.mutation_method == 'neuron':
                layer = random.randint(0, len(res.weights) - 1)                  # same logic here
                neuron = random.randint(0, len(res.weights[layer]) - 1)
                new_neuron = np.random.randn(len(res.weights[layer][neuron]))
                res.weights[layer][neuron] = new_neuron
        else:                                                      # mutation over bias
            layer = random.randint(0, len(res.biases) - 1)         # random layer
            bias = random.randint(0, len(res.biases[layer]) - 1)   # random bias
            res.weights[layer][bias] = np.random.randn()           # mutation
        return res

    def print_generation(self, networks, gen):
        """
        Prints facts about the current generation:
        - Best fitness
        - Pop size
        - Top 6 average
        - Bottom 6 average
        """
        top_mean = int(np.mean([networks[i].score for i in range(6)]))
        bottom_mean = int(np.mean([networks[-i].score for i in range(1, 6)]))
        print("\nBest Fitness gen", gen, " : ", networks[0].score)
        print("Pop size = ", len(networks))
        print("Average top 6 = ", top_mean)
        print("Average last 6 = ", bottom_mean)
