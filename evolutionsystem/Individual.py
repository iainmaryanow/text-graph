class Individual:
  def __init__(self, genes):
    self._genes = genes
    self._fitness_score = None


  def get_genes(self):
    return self._genes


  def get_fitness_score(self):
    return self._fitness_score


  def calculate_fitness_score(self, fitness_fn):
    self._fitness_score = fitness_fn(self._genes)