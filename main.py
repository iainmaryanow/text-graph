import math
from Graph import Graph
from evolutionsystem.EvolutionSystem import EvolutionSystem

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

def line_eq(point1, point2):
  if point2[0] - point1[0] == 0:
    return 9999, -9999

  slope = (point2[1] - point1[1]) / (point2[0] - point1[0])
  intercept = point2[1] - (slope * point2[0])
  return slope, intercept


def lines_intersect(points1, points2):
  slope1, intercept1 = line_eq(points1[0], points1[1])
  slope2, intercept2 = line_eq(points2[0], points2[1])
  if slope1 == slope2:
    return False

  x = (intercept2 - intercept1) / (slope1 - slope2)

  min_1 = min(points1[0][0], points1[1][0])
  max_1 = max(points1[0][0], points1[1][0])

  min_2 = min(points2[0][0], points2[1][0])
  max_2 = max(points2[0][0], points2[1][0])

  return x >= min_1 and x <= max_1 and x >= min_2 and x <= max_2


def get_intersecting_edges(solution, edges):
  ls = set()

  for node1 in edges.keys():
    for node2 in edges[node1]:
      points = (solution[mapping[node1]], solution[mapping[node2]])
      ls.add(points)

  intersections = []
  for points1 in ls:
    for points2 in ls:
      same = points1 == points2 or points1[0] in points2 or points1[1] in points2
      if not same and lines_intersect(points1, points2):
        intersections.append((points1, points2))

  return intersections


def get_average_distance_between_nodes(solution):
  min_dist = float('inf')
  dist = 0
  dists = []
  for i in solution:
    for j in solution:
      if i != j:
        dist += math.sqrt((j[0] - i[0])**2 + (j[1] - i[1])**2)
        dists.append(math.sqrt((j[0] - i[0])**2 + (j[1] - i[1])**2))
        if dist < min_dist:
          min_dist = dist
  return (dist / len(solution), min_dist, sorted(dists)[len(dists)//2])


def get_median_angle(intersecting_edges):
  angles = []
  for points1, points2 in intersecting_edges:
    angles.append(get_angle(points1, points2))
  return sorted(angles)[len(angles)//2]


def get_angle(points1, points2):
  angle1 = math.atan2(points1[0][1] - points1[1][1], points1[0][0] - points1[1][0])
  angle2 = math.atan2(points2[0][1] - points2[1][1], points2[0][0] - points2[1][0])
  return abs(math.degrees(abs(angle1) - abs(angle2)))


def get_distances_to_lines(solution, edges):
  ls = set()
  for node1 in edges.keys():
    for node2 in edges[node1]:
      points = (solution[mapping[node1]], solution[mapping[node2]])
      ls.add(points)

  min_dist = float('inf')
  dists = []
  for pos in solution:
    for points in ls:
      if pos not in points:
        dist = get_distance_to_line(pos, points)
        dists.append(dist)
        if dist < min_dist:
          min_dist = dist

  return (sum(dists) / len(dists), min_dist)


def get_distance_to_line(point, line):
  x = point[0]
  y = point[1]

  x1 = line[0][0]
  y1 = line[0][1]

  x2 = line[1][0]
  y2 = line[1][1]

  A = x - x1
  B = y - y1
  C = x2 - x1
  D = y2 - y1

  dot = A * C + B * D
  len_sq = C * C + D * D
  param = dot / len_sq

  if param < 0: # Projection is off the line segment, closest to line[0]
    xx = x1
    yy = y1
  elif param > 1: # Projection is off the line segment, closest to line[1]
    xx = x2
    yy = y2
  else: # Projection is somewhere on the line segment
    xx = x1 + param * C
    yy = y1 + param * D

  dx = x - xx
  dy = y - yy
  return math.sqrt(dx * dx + dy * dy) # Distance to closest point on line segment
  

def print_grid(grid):
  print(' ' + '_' * len(grid))
  for row in grid:
    print('|' + ''.join(row) + '|')
  print(' ' + '-' * len(grid))


def draw_line(grid, start, end, char='*'):
  slope, _ = line_eq(start, end)

  x_mov = 1
  if slope > len(grid):
    slope = 1
    x_mov = 0

  if start[0] > end[0]:
    x_mov *= -1

  if start[1] < end[1]:
    slope = abs(slope)
  else:
    slope = -abs(slope)

  x = start[0] + x_mov
  y = math.floor(start[1] + slope)

  while x <= max(start[0], end[0]) and x >= min(start[0], end[0]) and y <= max(start[1], end[1]) and y >= min(start[1], end[1]):
    if grid[math.floor(y)][x] == ' ':
      grid[math.floor(y)][x] = char
    x += x_mov
    y += slope


def draw(solution, edges, grid_size=50):
  grid = []
  for i in range(grid_size):
    grid.append([])
    for j in range(grid_size):
      grid[i].append(' ')

  xs = list(map(lambda s: s[0], solution))
  ys = list(map(lambda s: s[1], solution))
  min_x, max_x = min(xs), max(xs)
  min_y, max_y = min(ys), max(ys)

  updated_solution = []
  for i, p in enumerate(solution):
    perc_x = (p[0] - min_x) / (max_x - min_x)
    perc_y = (p[1] - min_y) / (max_y - min_y)

    x = math.floor((len(grid) - 1) * perc_x)
    y = math.floor((len(grid) - 1) * perc_y)
    updated_solution.append((x, y))
    grid[y][x] = str(i)

  chars = '*#@%=+><:'
  counter = 0

  drawn = set()
  for node1 in edges.keys():
    for node2 in edges[node1]:
      tup = tuple(sorted((node1, node2)))
      if not tup in drawn:
        draw_line(grid, updated_solution[mapping[node1]], updated_solution[mapping[node2]], chars[counter])
        drawn.add(tup)
        counter = (counter+1) % len(chars)

  print_grid(grid)



# TODO
# Clean up
# Fix edge angle only between intersecting edges, should be for two lines from same node
# Incorporate into Graph
# Figure out mapping between node and index
# Use other repo for evolutionsystem
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

  def fitness_fn(solution):
    # Don't allow overlapping nodes
    for i, s1 in enumerate(solution):
      for j, s2 in enumerate(solution):
        if i != j and s1[0] == s2[0] and s1[1] == s2[1]:
          return 0

    avg_dist_to_line, min_dist_to_line = get_distances_to_lines(solution, graph._edges)
    intersecting_edges = get_intersecting_edges(solution, graph._edges)
    dist, min_dist, median_dist = get_average_distance_between_nodes(solution)

    median_angle = 1
    if len(intersecting_edges):
      median_angle = get_median_angle(intersecting_edges)

    return (median_dist * median_angle * avg_dist_to_line * min_dist_to_line * min_dist) / (len(intersecting_edges) + 1)

  number_of_individuals = 400
  number_of_genes = len(graph._edges.keys())
  number_of_generations = 40
  p_mutation = .5
  mutation_dev = 3

  ea = EvolutionSystem(fitness_fn, number_of_individuals, number_of_genes, p_mutation, mutation_dev)
  ea.evolve(number_of_generations)
  ind = ea.get_best_evolved_individual()

  draw(ind.get_genes(), graph._edges)