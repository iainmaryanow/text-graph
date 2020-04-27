import math
from Graph import Graph
from evolutionsystem.EvolutionSystem import EvolutionSystem
from LineSegment import LineSegment
from Point import Point

GRID_EMPTY = ' '
GRID_SIDE_BORDER = '|'
GRID_BOTTOM_BORDER = '─'
GRID_TOP_BORDER = '_'
GRID_LINE_CHARS = ['⌾', '○', '●', '⦵', '𐩑', '*', '+']

mapping = {
  'Jeju': 0,
  'Busan': 1,
  'SeoulMetro': 2,
  'Pohang': 3,
  'Seoul': 4,
  'Cheongju': 5,
  'Sacheon': 6,
  'Daegu': 7
}

def get_intersecting_edges(solution, edges):
  lines = set()
  for node1 in edges.keys():
    for node2 in edges[node1]:
      lines.add(LineSegment(solution[mapping[node1]], solution[mapping[node2]]))

  intersections = []
  for line_1 in lines:
    for line_2 in lines:
      same = line_1 == line_2 or line_1.contains_point(line_2.point_1) or line_1.contains_point(line_2.point_2)
      if not same and line_1.is_intersecting(line_2):
        intersections.append((line_1, line_2))

  return intersections


def get_average_distance_between_nodes(solution):
  min_dist = float('inf')
  dist = 0
  dists = []
  for point_1 in solution:
    for point_2 in solution:
      if point_1 != point_2:
        distance = point_1.calculate_distance_to_point(point_2)
        dist += distance
        dists.append(distance)
        if distance < min_dist:
          min_dist = distance
  return (dist / len(solution), min_dist, sorted(dists)[len(dists)//2])


def get_median_angle(solution, edges):
  lines = set()
  for node1 in edges.keys():
    for node2 in edges[node1]:
      lines.add(LineSegment(solution[mapping[node1]], solution[mapping[node2]]))

  angles = []
  for line_1 in lines:
    for line_2 in lines:
      if line_1 != line_2 and line_1.contains_point(line_2.point_1) or line_1.contains_point(line_2.point_2):
          angles.append(line_1.calculate_angle_with_line(line_2))
  return sorted(angles)[len(angles)//2]


def get_distances_to_lines(solution, edges):
  lines = set()
  for node1 in edges.keys():
    for node2 in edges[node1]:
      lines.add(LineSegment(solution[mapping[node1]], solution[mapping[node2]]))

  min_dist = float('inf')
  dists = []
  for pos in solution:
    for line in lines:
      if not line.contains_point(pos):
        dist = pos.calculate_distance_to_line_segment(line)
        dists.append(dist)
        if dist < min_dist:
          min_dist = dist

  return (sum(dists) / len(dists), min_dist)
  

def print_grid(grid):
  print(GRID_EMPTY + GRID_TOP_BORDER * len(grid))
  for row in grid:
    print(GRID_SIDE_BORDER + ''.join(row) + GRID_SIDE_BORDER)
  print(GRID_EMPTY + GRID_BOTTOM_BORDER * len(grid))


def draw_line(grid, line, char='*'):
  slope = line.slope

  x_mov = 1
  if slope > len(grid):
    slope = 1
    x_mov = 0

  if line.point_1.x > line.point_2.x:
    x_mov *= -1

  if line.point_1.y < line.point_2.y:
    slope = abs(slope)
  else:
    slope = -abs(slope)

  x = line.point_1.x + x_mov
  y = math.floor(line.point_1.y + slope)

  while x <= max(line.point_1.x, line.point_2.x) and x >= min(line.point_1.x, line.point_2.x) and y <= max(line.point_1.y, line.point_2.y) and y >= min(line.point_1.y, line.point_2.y):
    if grid[math.floor(y)][x] == GRID_EMPTY:
      grid[math.floor(y)][x] = char
    x += x_mov
    y += slope


def get_bounding_box(solution):
  x_values = list(map(lambda s: s.x, solution))
  y_values = list(map(lambda s: s.y, solution))
  return min(x_values), min(y_values), max(x_values), max(y_values)


def draw(solution, edges, grid_size=50):
  grid = [[GRID_EMPTY for _ in range(grid_size)] for _ in range(grid_size)]
  min_x, min_y, max_x, max_y = get_bounding_box(solution)

  scaled_solution = []
  for i, p in enumerate(solution):
    perc_x = (p.x - min_x) / (max_x - min_x)
    perc_y = (p.y - min_y) / (max_y - min_y)

    x = math.floor((len(grid) - 1) * perc_x)
    y = math.floor((len(grid) - 1) * perc_y)
    scaled_solution.append(Point(x, y))
    grid[y][x] = str(i)

  counter = 0
  drawn = set()
  for node1 in edges.keys():
    for node2 in edges[node1]:
      tup = tuple(sorted((node1, node2)))
      if not tup in drawn:
        line = LineSegment(scaled_solution[mapping[node1]], scaled_solution[mapping[node2]])
        draw_line(grid, line, GRID_LINE_CHARS[counter])
        drawn.add(tup)
        counter = (counter+1) % len(GRID_LINE_CHARS)

  print_grid(grid)



# TODO
# Clean up
# Incorporate into Graph
# Figure out mapping between node and index
# Use other repo for evolutionsystem
# verbose
# Completely draw line on vertical or horizontal
if __name__ == '__main__':

  graph = Graph()
  graph.add_node('Jeju')
  graph.add_node('Busan')
  graph.add_node('SeoulMetro')
  graph.add_node('Pohang')
  graph.add_node('Seoul')
  graph.add_node('Cheongju')
  graph.add_node('Sacheon')
  graph.add_node('Daegu')

  graph.add_edge('Jeju', 'Cheongju', undirected=True)
  graph.add_edge('Jeju', 'Busan', undirected=True)
  graph.add_edge('Jeju', 'Daegu', undirected=True)
  graph.add_edge('Jeju', 'Sacheon', undirected=True)
  graph.add_edge('Busan', 'SeoulMetro', undirected=True)
  graph.add_edge('Busan', 'Seoul', undirected=True)
  graph.add_edge('Pohang', 'Seoul', undirected=True)
  graph.add_edge('Sacheon', 'Seoul', undirected=True)
  graph.add_edge('Seoul', 'Daegu', undirected=True)
  graph.add_edge('SeoulMetro', 'Daegu', undirected=True)

  # Needs graph._edges
  def fitness_fn(solution):
    avg_dist_to_line, min_dist_to_line = get_distances_to_lines(solution, graph._edges)
    intersecting_edges = get_intersecting_edges(solution, graph._edges)
    dist, min_dist, median_dist = get_average_distance_between_nodes(solution)
    median_angle = get_median_angle(solution, graph._edges)
    return (median_dist * median_angle * avg_dist_to_line * min_dist_to_line * min_dist) / (len(intersecting_edges) + 1)


  number_of_individuals = 400
  number_of_genes = len(graph._edges.keys())
  number_of_generations = 20
  p_mutation = .4
  mutation_dev = 3

  ea = EvolutionSystem(fitness_fn, number_of_individuals, number_of_genes, p_mutation, mutation_dev)
  ea.evolve(number_of_generations)
  ind = ea.get_best_evolved_individual()

  draw(ind.get_genes(), graph._edges)