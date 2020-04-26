class Graph:
  def __init__(self):
    self._edges = {}


  def add_node(self, node):
    if node in self._edges:
      raise Exception('Node (%s) already exists' % str(node))

    self._edges[node] = {}
    return self


  def remove_node(self, node):
    self._check_node_exists(node)
    del self._edges[node]

    for other_node in self._edges.keys():
      if node in self._edges[other_node]:
        del self._edges[other_node][node]


  def add_edge(self, source, dest, undirected=False, weight=1):
    self._check_node_exists(source)
    self._edges[source][dest] = weight

    if undirected:
      self._check_node_exists(dest)
      self._edges[dest][source] = weight


  def remove_edge(self, source, dest):
    self._check_node_exists(source)
    self._check_node_exists(dest)

    # Directed
    if dest in self._edges[source]:
      del self._edges[source][dest]

    # Undirected
    if source in self._edges[dest]:
      del self._edges[dest][source]


  def get_neighbors(self, node, undirected=False):
    self._check_node_exists(node)
    neighbors = set(self._edges[node].keys())

    if undirected:
      for other_node in self._edges.keys():
        if node in self._edges[other_node]:
          neighbors.add(other_node)

    return neighbors


  def reset(self):
    self._edges = {}


  def _check_node_exists(self, node):
    if node not in self._edges:
      raise Exception('Node (%s) does not exist' % str(node))