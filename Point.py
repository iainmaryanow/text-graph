import math
from LineSegment import LineSegment

class Point:
  def __init__(self, x, y):
    self.x = x
    self.y = y


  def __eq__(self, other):
    if not isinstance(other, type(self)):
      return NotImplemented
    return self.x == other.x and self.y == other.y


  def __hash__(self):
    return hash((self.x, self.y))


  def create_line_with_point(self, point):
    return LineSegment(self, point)


  def calculate_distance_to_line_segment(self, line_segment):
    x1, y1 = line_segment.point_1.x, line_segment.point_1.y
    x2, y2 = line_segment.point_2.x, line_segment.point_2.y

    point_line_x_diff = self.x - x1
    point_line_y_diff = self.y - y1
    line_segment_x_diff = x2 - x1
    line_segment_y_diff = y2 - y1

    dot = (point_line_x_diff * line_segment_x_diff) + (point_line_y_diff * line_segment_y_diff)
    line_segment_length = line_segment_x_diff**2 + line_segment_y_diff**2
    percentage_onto_line_segment = -1 if line_segment_length == 0 else dot / line_segment_length

    if percentage_onto_line_segment < 0: # Projection is off the line segment, closest to line_segment.point_1
      closest_x = x1
      closest_y = y1
    elif percentage_onto_line_segment > 1: # Projection is off the line segment, closest to line_segment.point_2
      closest_x = x2
      closest_y = y2
    else: # Projection is somewhere on the line segment
      closest_x = x1 + percentage_onto_line_segment * line_segment_x_diff
      closest_y = y1 + percentage_onto_line_segment * line_segment_y_diff

    x_diff = self.x - closest_x
    y_diff = self.y - closest_y
    return math.sqrt(x_diff**2 + y_diff**2) # Distance to closest point on line segment


  def calculate_distance_to_point(self, point):
    return math.sqrt((self.x - point.x)**2 + (self.y - point.y)**2)