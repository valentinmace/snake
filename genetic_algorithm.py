import copy
import numpy as np
import random
import multiprocessing
from random import randint
from pygame.locals import *
from game import*
from neural_network import *
from joblib import Parallel, delayed

class Genetic:

  def __init__(self, networks=None, networks_number=150, networks_shape=[14,16,3], crossover_rate=0.3,
               crossover_method='neuron', mutation_rate=0.7, mutation_method='neuron'):
    self.networks = networks
    if networks is None:
      self.networks = []
      for i in range(networks_number):
        self.networks.append(Network(networks_shape))
    self.population_size = networks_number
    self.crossover_rate = crossover_rate
    self.crossover_number = int(self.crossover_rate*self.population_size)
    self.crossover_method = crossover_method
    self.mutation_rate = mutation_rate
    self.mutation_number = int(self.mutation_rate*self.population_size)
    self.mutation_method = mutation_method
    self.networks_shape = networks_shape

  def start(self):
    networks = self.networks
    population_size = self.population_size
    crossover_number = self.crossover_number
    mutation_number = self.mutation_number

    num_cores = multiprocessing.cpu_count()
    gen = 0
    for i in range(100):
      gen+=1
      parents = []
      for i in range(crossover_number):
        parent = self.tournament(networks[randint(0, population_size - 1)],
                                 networks[randint(0, population_size - 1)],
                                 networks[randint(0, population_size - 1)])
        parents.append(parent)

      childs = []
      for i in range(crossover_number):
        child = self.crossover(parents[randint(0, crossover_number - 1)],
                               parents[randint(0, crossover_number - 1)])
        childs.append(child)

      mutations = []
      for i in range(mutation_number):
        mut = self.mutation(networks[randint(0, population_size - 1)])
        mutations.append(mut)

      networks = networks + childs + mutations
      game = Game()
      # for i in range(len(self.networks)):
      #   self.networks[i].score = game.start(network=self.networks[i])
      results = Parallel(n_jobs=num_cores)(delayed(game.start_invisible)(neural_net=networks[i]) for i in range(len(networks)))
      results2 = Parallel(n_jobs=num_cores)(delayed(game.start_invisible)(neural_net=networks[i]) for i in range(len(networks)))
      results3 = Parallel(n_jobs=num_cores)(delayed(game.start_invisible)(neural_net=networks[i]) for i in range(len(networks)))
      results4 = Parallel(n_jobs=num_cores)(delayed(game.start_invisible)(neural_net=networks[i]) for i in range(len(networks)))

      for i in range(len(results)):
        networks[i].score = int(np.mean([results[i], results2[i], results3[i], results4[i]]))

      networks.sort(key=lambda Network: Network.score, reverse=True)
      if(networks[0].score>40000):
        networks[0].save()

      for i in range(int(0.2*len(networks))):                                   #TEST Mutation supplémentaire
        rand = randint(10, len(networks)-1)
        networks[rand] = self.mutation(networks[rand])
      networks = networks[:population_size]                      #TEST On rajoute des réseaux random à la fin

      print("\nBest Fitness gen", gen, " : ", networks[0].score)
      print("Pop size = ", len(networks))
      print("Average top 6 = ", int(np.mean([networks[0].score, networks[1].score, networks[2].score,
                                             networks[3].score, networks[4].score,
                                             networks[5].score, ])))
      print("Average last 6 = ", int(np.mean([networks[-1].score, networks[-2].score, networks[-3].score,
                                              networks[-4].score, networks[-5].score,
                                              networks[-6].score, ])))




  def tournament(self, net1, net2, net3):
    game = Game()
    game.start_invisible(neural_net=net1)
    score1 = game.game_score
    game.start_invisible(neural_net=net2)
    score2 = game.game_score
    game.start_invisible(neural_net=net3)
    score3 = game.game_score
    maxscore = max(score1,score2,score3)
    if maxscore == score1:
      return net1
    elif maxscore == score2:
      return net2
    else:
      return net3

  def crossover(self, net1, net2):
    res1 = copy.deepcopy(net1)
    res2 = copy.deepcopy(net2)
    weights_or_biases = random.randint(0, 1)
    if weights_or_biases == 0:
      if(self.crossover_method == 'weight'):
        layer = random.randint(0, len(res1.weights) - 1)
        neuron = random.randint(0, len(res1.weights[layer]) - 1)
        weight = random.randint(0, len(res1.weights[layer][neuron]) - 1)
        temp = res1.weights[layer][neuron][weight]
        res1.weights[layer][neuron][weight] = res2.weights[layer][neuron][weight]
        res2.weights[layer][neuron][weight] = temp
      elif(self.crossover_method == 'neuron'):
        layer = random.randint(0, len(res1.weights) - 1)
        neuron = random.randint(0, len(res1.weights[layer]) - 1)
        temp = copy.deepcopy(res1)
        res1.weights[layer][neuron] = res2.weights[layer][neuron]
        res2.weights[layer][neuron] = temp.weights[layer][neuron]
      elif(self.crossover_method == 'layer'):
        layer = random.randint(0, len(res1.weights) - 1)
        temp = copy.deepcopy(res1)
        res1.weights[layer] = res2.weights[layer]
        res2.weights[layer] = temp.weights[layer]
    else:
      layer = random.randint(0, len(res1.biases) - 1)
      bias = random.randint(0, len(res1.biases[layer]) - 1)
      temp = copy.deepcopy(res1)
      res1.biases[layer][bias] = res2.biases[layer][bias]
      res2.biases[layer][bias] = temp.biases[layer][bias]

    game = Game()
    game.start_invisible(neural_net=res1)
    score1 = game.game_score
    game.start_invisible(neural_net=res2)
    score2 = game.game_score
    if(score1>score2):
      return res1
    else:
      return res2

  def mutation(self, net):
    res = copy.deepcopy(net)
    weights_or_biases = random.randint(0, 1)
    if weights_or_biases == 0:
      if self.mutation_method == 'weight':
        layer = random.randint(0, len(res.weights) - 1)
        neuron = random.randint(0, len(res.weights[layer]) - 1)
        weight = random.randint(0, len(res.weights[layer][neuron]) - 1)
        res.weights[layer][neuron][weight] = np.random.randn()
      elif self.mutation_method == 'neuron':
        layer = random.randint(0, len(res.weights) - 1)
        neuron = random.randint(0, len(res.weights[layer]) - 1)
        new_neuron = np.random.randn(len(res.weights[layer][neuron]))
        res.weights[layer][neuron] = new_neuron
    else:
      layer = random.randint(0, len(res.biases) - 1)
      bias = random.randint(0, len(res.biases[layer]) - 1)
      res.weights[layer][bias] = np.random.randn()
    return res

# Reproduction
# Soit on swap un weight d'un neurone entre deux parents,
# soit on swap tous les weights pour un neurone
# soit on swap tous les weights d'un layer (inutile si trop peu de layers)
# dans tous les cas on fait 2 enfants et on sélectionne le meilleur

# Mutation
# Opère sur un seul weight
# soit on le remplace avec une valeur aléatoire
# soit on le change par un %, on le multiplie par un nb entre 0-2 (ou 0.5-1.5)
# on ajoute ou soustrait un nombre aléatoire entre 0 et 1
# on change le signe
# on swap les weights d'un neurone
