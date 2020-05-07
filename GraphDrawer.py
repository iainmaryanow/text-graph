import math
from evolutionsystem.EvolutionSystem import EvolutionSystem
from FitnessCalculator import FitnessCalculator
from Point import Point

GRID_EMPTY = ' '
GRID_SIDE_BORDER = '|'
GRID_BOTTOM_BORDER = '─'
GRID_TOP_BORDER = '_'
GRID_LINE_CHARS = ['⌾', '○', '●', '⦵', '𐩑', '*', '+', '◇']

class GraphDrawer:
  def __init__(self, graph, number_of_individuals=200, number_of_genes=None, number_of_generations=25, p_mutation=.4, mutation_dev=3):
    if number_of_genes is None:
      number_of_genes = len(graph._edges.keys())

    self._graph = graph
    self._number_of_individuals = number_of_individuals
    self._number_of_genes = number_of_genes
    self._number_of_generations = number_of_generations
    self._p_mutation = p_mutation
    self._mutation_dev = mutation_dev
    self._layout = self._solve_graph_layout()


  def _solve_graph_layout(self):
    evolution_system = EvolutionSystem(
      FitnessCalculator.fitness_fn_wrapper(self._graph),
      self._number_of_individuals,
      self._number_of_genes,
      self._p_mutation,
      self._mutation_dev
    )
    evolution_system.evolve(self._number_of_generations)
    return evolution_system.get_best_evolved_individual().get_genes()


  def _get_bounding_box(self):
    x_values = list(map(lambda s: s.x, self._layout))
    y_values = list(map(lambda s: s.y, self._layout))
    return min(x_values), min(y_values), max(x_values), max(y_values)


  def _draw_line(self, grid, line, char='*'):
    slope = line.slope

    x_mov = 1

    # Undefined slope
    if slope > len(grid):
      slope = 1
      x_mov = 0

    if line.point_1.x > line.point_2.x:
      x_mov *= -1

    slope = abs(slope)
    if line.point_1.y > line.point_2.y:
      slope = -abs(slope)

    x = line.point_1.x + x_mov
    y = math.floor(line.point_1.y + slope)

    while x <= max(line.point_1.x, line.point_2.x) and x >= min(line.point_1.x, line.point_2.x) and y <= max(line.point_1.y, line.point_2.y) and y >= min(line.point_1.y, line.point_2.y):
      if grid[math.floor(y)][x] == GRID_EMPTY:
        grid[math.floor(y)][x] = char
      x += x_mov
      y += slope


  def _print_grid(self, grid):
    print(GRID_EMPTY + GRID_TOP_BORDER * len(grid))
    for row in grid:
      print(GRID_SIDE_BORDER + ''.join(row) + GRID_SIDE_BORDER)
    print(GRID_EMPTY + GRID_BOTTOM_BORDER * len(grid))


  def draw(self, grid_size=50):
    grid = [[GRID_EMPTY for _ in range(grid_size)] for _ in range(grid_size)]
    min_x, min_y, max_x, max_y = self._get_bounding_box()

    scaled_layout = []
    for i, p in enumerate(self._layout):
      perc_x = (p.x - min_x) / (max_x - min_x)
      perc_y = (p.y - min_y) / (max_y - min_y)

      x = math.floor((len(grid) - 1) * perc_x)
      y = math.floor((len(grid) - 1) * perc_y)
      scaled_layout.append(Point(x, y))
      grid[y][x] = str(i)

    lines = FitnessCalculator.build_line_segments(scaled_layout, self._graph._edges, self._graph._nodes)
    for index, line in enumerate(lines):
      line_character = GRID_LINE_CHARS[index % len(GRID_LINE_CHARS)]
      self._draw_line(grid, line, line_character)

    self._print_grid(grid)