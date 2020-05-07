from LineSegment import LineSegment
from Point import Point

class FitnessCalculator:

  @staticmethod
  def fitness_fn_wrapper(graph):

    def fitness_fn(potential_layout):
      lines = FitnessCalculator.build_line_segments(potential_layout, graph._edges, graph._nodes)
      average_distance_to_line = FitnessCalculator._get_distances_to_lines(potential_layout, lines)
      intersecting_edges = FitnessCalculator._get_intersecting_edges(lines)
      average_distance_to_node = FitnessCalculator._get_average_distance_between_nodes(potential_layout)
      average_angle = FitnessCalculator._get_average_angle(lines)
      return (average_angle * average_distance_to_line * average_distance_to_node) / (intersecting_edges + 1)

    return fitness_fn


  @staticmethod
  def build_line_segments(layout, edges, nodes):
    node_mapping = {node: index for index, node in enumerate(nodes)}

    lines = set()
    for node1 in edges.keys():
      for node2 in edges[node1]:
        lines.add(LineSegment(layout[node_mapping[node1]], layout[node_mapping[node2]]))
    return lines


  @staticmethod
  def _get_intersecting_edges(lines):
    intersections = 0
    for line_1 in lines:
      for line_2 in lines:
        # Dont consider intersecting if they start or end at the same point
        same = line_1 == line_2 or line_1.contains_point(line_2.point_1) or line_1.contains_point(line_2.point_2)
        if not same and line_1.is_intersecting(line_2):
          intersections += 1
    return intersections


  @staticmethod
  def _get_average_distance_between_nodes(layout):
    distances = []
    for point_1 in layout:
      for point_2 in layout:
        if point_1 != point_2:
          distances.append(point_1.calculate_distance_to_point(point_2))
    return sum(distances) / len(distances)


  @staticmethod
  def _get_average_angle(lines):
    angles = []
    for line_1 in lines:
      for line_2 in lines:
        if line_1.contains_point(line_2.point_1) or line_1.contains_point(line_2.point_2):
            angles.append(line_1.calculate_angle_with_line(line_2))
    return sum(angles) / len(angles)


  @staticmethod
  def _get_distances_to_lines(layout, lines):
    distances = []
    for pos in layout:
      for line in lines:
        if not line.contains_point(pos):
          distances.append(pos.calculate_distance_to_line_segment(line))
    return sum(distances) / len(distances)