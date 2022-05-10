import math

class LineSegment:
  def __init__(self, point_1, point_2):
    self.point_1 = point_1
    self.point_2 = point_2
    self.slope, self.intercept = self._calculate_slope_and_intercept()


  def __eq__(self, other):
    if not isinstance(other, type(self)):
      return NotImplemented

    matches_point_1 = other.point_1 == self.point_1 or other.point_1 == self.point_2
    matches_point_2 = other.point_2 == self.point_1 or other.point_2 == self.point_2

    return matches_point_1 and matches_point_2


  def __hash__(self):
    return hash(frozenset([self.point_1, self.point_2]))


  def contains_point(self, point):
    return self.point_1 == point or self.point_2 == point


  def is_intersecting(self, line_segment):
    if self.slope == line_segment.slope:
      if self.point_1.calculate_distance_to_line_segment(line_segment) == 0 or self.point_2.calculate_distance_to_line_segment(line_segment) == 0:
        return True
      return False

    x_intersection = (line_segment.intercept - self.intercept) / (self.slope - line_segment.slope)

    min_x_self = min(self.point_1.x, self.point_2.x)
    max_x_self = max(self.point_1.x, self.point_2.x)

    min_x_line = min(line_segment.point_1.x, line_segment.point_2.x)
    max_x_line = max(line_segment.point_1.x, line_segment.point_2.x)

    return x_intersection >= min_x_self \
       and x_intersection <= max_x_self \
       and x_intersection >= min_x_line \
       and x_intersection <= max_x_line


  def calculate_angle_with_line(self, line_segment):
    angle1 = math.atan2(self.point_1.y - self.point_2.y, self.point_1.x - self.point_2.x)
    angle2 = math.atan2(line_segment.point_1.y - line_segment.point_2.y, line_segment.point_1.x - line_segment.point_2.x)
    return abs(math.degrees(abs(angle1) - abs(angle2)))


  def _calculate_slope_and_intercept(self):
    # Infinite slope when the two points are stacked
    if self.point_2.x - self.point_1.x == 0:
      # return float('inf'), None
      return 9999, -9999

    slope = (self.point_2.y - self.point_1.y) / (self.point_2.x - self.point_1.x)
    intercept = self.point_2.y - (slope * self.point_2.x)
    return slope, intercept