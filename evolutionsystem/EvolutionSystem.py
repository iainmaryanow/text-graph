from random import random, randint, gauss
from evolutionsystem.Individual import Individual

class EvolutionSystem:
  def __init__(self, fitness_fn, number_of_individuals=20, number_of_genes=10, probability_of_mutation=.25, mutation_deviation=2):
    self._fitness_fn = fitness_fn
    self._number_of_genes = number_of_genes
    self._probability_of_mutation = probability_of_mutation
    self._mutation_deviation = mutation_deviation
    self._population = self._initialize_population(number_of_individuals)


  def evolve(self, number_of_generations=10):
    for _ in range(number_of_generations):
      self._calculate_fitness_scores()
      self._update_population()
      parent_pairs = self._pair_individuals()
      children = self._mate_parents(parent_pairs)
      self._population += children


  def get_best_evolved_individuals(self, number_of_individuals=1):
    self._calculate_fitness_scores()
    self._order_population_by_fitness_score()
    return self._population[:number_of_individuals]


  def _initialize_population(self, number_of_individuals):
    population = []
    for _ in range(number_of_individuals):
      genes = [(randint(-9, 9), randint(-9, 9)) for _ in range(self._number_of_genes)]
      population.append(Individual(genes))
    return population


  def _calculate_fitness_scores(self):
    for individual in self._population:
      individual.calculate_fitness_score(self._fitness_fn)


  def _update_population(self):
    self._order_population_by_fitness_score()
    self._population = self._population[:len(self._population)//2]


  def _order_population_by_fitness_score(self):
    self._population.sort(reverse=True, key=lambda individual: individual.get_fitness_score())


  def _pair_individuals(self):
    parents = []
    for i in range(len(self._population)//2):
      parents.append((self._population[2*i], self._population[2*i+1]))
    return parents


  def _mate_parents(self, parent_pairs):
    children = []
    for parent_1, parent_2 in parent_pairs:
      child_1 = self._create_child(parent_1, parent_2)
      child_2 = self._create_child(parent_2, parent_1)

      children.append(child_1)
      children.append(child_2)

    return children


  def _create_child(self, parent_1, parent_2):
    pivot_gene = randint(0, self._number_of_genes-1)
    genes = parent_1.get_genes()[:pivot_gene] + parent_2.get_genes()[pivot_gene:]

    if random() <= self._probability_of_mutation:
      gene_index = randint(0, self._number_of_genes-1)
      allele1 = round(gauss(genes[gene_index][0], self._mutation_deviation))
      allele2 = round(gauss(genes[gene_index][1], self._mutation_deviation))
      genes[gene_index] = (allele1, allele2)

    return Individual(genes)