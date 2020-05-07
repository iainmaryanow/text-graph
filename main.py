from Graph import Graph
from GraphDrawer import GraphDrawer


# TODO
# Allow directed edges
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

  graph_drawer = GraphDrawer(graph)
  graph_drawer.draw()